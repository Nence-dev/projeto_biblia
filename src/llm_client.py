"""Cliente resiliente da Google Gemini API para geração de estudos teológicos expositivos."""

from __future__ import annotations

import logging
import time
from typing import Callable, Optional

from src.config import validate_api_key, GEMINI_MODEL, ConfigError
from src.prompts import (
    SYSTEM_PROMPT_TEOLOGICO,
    SYSTEM_PROMPT_DEVOCIONAL,
    montar_prompt_usuario,
    montar_prompt_whatsapp,
    montar_prompt_minuto,
)

logger = logging.getLogger(__name__)

# Modelos recomendados para fallback estático (família Gemini 2.x e 1.5)
MODELOS_PADRAO_FALLBACK = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-pro",
]


class LLMError(Exception):
    """Exceção levantada em erros de comunicação ou geração com a LLM."""
    pass


class GeminiClient:
    """Cliente resiliente para interagir com a API Google Gemini com retry e fallback automático."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or validate_api_key()
        self.model_name = model_name or GEMINI_MODEL
        self._init_sdk()

    def _init_sdk(self) -> None:
        """Inicializa o cliente google-genai com fallback para google-generativeai."""
        try:
            # SDK oficial moderno (google-genai)
            from google import genai  # type: ignore
            from google.genai import types  # type: ignore

            self._client = genai.Client(api_key=self.api_key)
            self._use_new_sdk = True
            self._types = types
        except ImportError:
            try:
                # Fallback para o SDK legado (google-generativeai) caso instalado
                import google.generativeai as legacy_genai  # type: ignore

                legacy_genai.configure(api_key=self.api_key)
                self._legacy_genai = legacy_genai
                self._use_new_sdk = False
            except ImportError as err:
                raise LLMError(
                    "Nenhuma biblioteca do Google Gemini foi encontrada.\n"
                    "Instale as dependências executando:\n"
                    "  pip install -r requirements.txt"
                ) from err

    def descobrir_modelos_disponiveis(self) -> list[str]:
        """Descobre dinamicamente na API do Google os modelos disponíveis para esta chave."""
        try:
            if self._use_new_sdk and hasattr(self._client, "models"):
                modelos_descobertos = []
                for m in self._client.models.list():
                    nome = getattr(m, "name", "") or ""
                    nome_limpo = nome.replace("models/", "").strip()
                    # Filtra apenas modelos compatíveis com geração de texto
                    if any(k in nome_limpo for k in ["flash", "pro", "gemini"]):
                        if not any(k in nome_limpo for k in ["embed", "vision", "tts", "imagen"]):
                            modelos_descobertos.append(nome_limpo)
                if modelos_descobertos:
                    return modelos_descobertos
        except Exception as exc:
            logger.debug(f"Não foi possível listar modelos dinamicamente: {exc}")
        return MODELOS_PADRAO_FALLBACK

    def _generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        on_status: Optional[Callable[[str], None]] = None,
    ) -> str:
        """Executa a chamada de geração com retry exponencial e fallback de modelos."""
        # Monta lista de prioridade de modelos
        modelos_para_tentar = [self.model_name]
        try:
            for m in self.descobrir_modelos_disponiveis():
                if m not in modelos_para_tentar:
                    modelos_para_tentar.append(m)
        except Exception:
            pass
        for m in MODELOS_PADRAO_FALLBACK:
            if m not in modelos_para_tentar:
                modelos_para_tentar.append(m)

        ultimo_erro = None

        for idx, modelo_atual in enumerate(modelos_para_tentar):
            max_tentativas = 3
            for tentativa in range(1, max_tentativas + 1):
                try:
                    if self._use_new_sdk:
                        config_kwargs = {
                            "temperature": 0.7,
                            "max_output_tokens": 8192,
                        }
                        if system_instruction:
                            config_kwargs["system_instruction"] = system_instruction

                        config = self._types.GenerateContentConfig(**config_kwargs)
                        response = self._client.models.generate_content(
                            model=modelo_atual,
                            contents=prompt,
                            config=config,
                        )
                        texto_resposta = response.text
                        if not texto_resposta or not texto_resposta.strip():
                            raise LLMError("A API do Gemini retornou uma resposta vazia.")

                        # Verificação anti-truncamento: estudos longos que começaram com as seções mas cortaram antes do fim
                        if len(texto_resposta) > 800 and ("### 1." in texto_resposta or "## 1." in texto_resposta) and "### 5." not in texto_resposta and "## 5." not in texto_resposta:
                            raise LLMError("A resposta gerada pelo modelo foi truncada antes da seção 5 de fechamento.")

                        self.model_name = modelo_atual
                        return texto_resposta
                    else:
                        # Caminho legado
                        model_kwargs = {
                            "model_name": modelo_atual,
                            "generation_config": {
                                "temperature": 0.7,
                                "max_output_tokens": 8192,
                            },
                        }
                        if system_instruction:
                            model_kwargs["system_instruction"] = system_instruction

                        model = self._legacy_genai.GenerativeModel(**model_kwargs)
                        response = model.generate_content(prompt)
                        texto_resposta = response.text
                        if not texto_resposta or not texto_resposta.strip():
                            raise LLMError("A API do Gemini retornou uma resposta vazia.")

                        if len(texto_resposta) > 800 and ("### 1." in texto_resposta or "## 1." in texto_resposta) and "### 5." not in texto_resposta and "## 5." not in texto_resposta:
                            raise LLMError("A resposta gerada pelo modelo foi truncada antes da seção 5 de fechamento.")

                        self.model_name = modelo_atual
                        return texto_resposta

                except Exception as exc:
                    ultimo_erro = exc
                    msg = str(exc)

                    # Erro fatal de autenticação
                    if "API_KEY_INVALID" in msg:
                        raise LLMError(f"Erro de autenticação na Gemini API: Chave inválida ({msg})") from exc

                    # Erro 404 (modelo inexistente ou descontinuado como 2.5-flash)
                    if "404" in msg or "not_found" in msg.lower():
                        logger.warning(f"Modelo '{modelo_atual}' indisponível para esta conta (404). Alternando modelo...")
                        break

                    # Erros transitórios de sobrecarga (503 UNAVAILABLE / 429 RESOURCE_EXHAUSTED)
                    eh_transitorio = (
                        "503" in msg
                        or "unavailable" in msg.lower()
                        or "high demand" in msg.lower()
                        or "429" in msg
                        or "resource_exhausted" in msg.lower()
                        or "temporarily" in msg.lower()
                    )

                    if eh_transitorio:
                        if tentativa < max_tentativas:
                            tempo_espera = tentativa * 3  # 3s, 6s
                            aviso = (
                                f"⚠️ Google Gemini sob alta demanda temporária (503). "
                                f"Aguardando {tempo_espera}s para retentar ({tentativa}/{max_tentativas})..."
                            )
                            logger.info(aviso)
                            if on_status:
                                on_status(aviso)
                            time.sleep(tempo_espera)
                            continue
                        else:
                            proximo = modelos_para_tentar[idx + 1] if idx + 1 < len(modelos_para_tentar) else None
                            if proximo:
                                aviso_alt = f"🔄 Modelo '{modelo_atual}' ocupado. Alternando automaticamente para '{proximo}'..."
                                logger.warning(aviso_alt)
                                if on_status:
                                    on_status(aviso_alt)
                            break
                    else:
                        # Outro erro inesperado
                        break

        msg_final = str(ultimo_erro) if ultimo_erro else "Erro desconhecido"
        if "503" in msg_final or "unavailable" in msg_final.lower():
            raise LLMError(
                "Os servidores do Google Gemini estão com alta demanda temporária (503 UNAVAILABLE).\n"
                "Picos de demanda na camada gratuita duram geralmente poucos segundos.\n"
                "Aguarde cerca de 10 a 20 segundos e tente novamente.\n"
                f"Detalhe retornado pelo Google: {msg_final}"
            ) from ultimo_erro

        raise LLMError(f"Falha na comunicação com o Gemini: {msg_final}") from ultimo_erro

    def gerar_estudo_completo(
        self,
        referencia: str,
        texto: str,
        versao: str,
        on_status: Optional[Callable[[str], None]] = None,
    ) -> str:
        """Gera a reflexão teológica expositiva estruturada em 5 etapas."""
        prompt_usuario = montar_prompt_usuario(referencia, texto, versao)
        return self._generate(
            prompt=prompt_usuario,
            system_instruction=SYSTEM_PROMPT_TEOLOGICO,
            on_status=on_status,
        )

    def gerar_derivacao_whatsapp(
        self,
        referencia: str,
        texto: str,
        versao: str,
        estudo_gerado: str,
        on_status: Optional[Callable[[str], None]] = None,
    ) -> str:
        """Gera uma versão sintetizada e atraente para WhatsApp / Redes Sociais."""
        prompt_whatsapp = montar_prompt_whatsapp(referencia, texto, versao, estudo_gerado)
        return self._generate(
            prompt=prompt_whatsapp,
            system_instruction=SYSTEM_PROMPT_TEOLOGICO,
            on_status=on_status,
        )

    def gerar_devocional_narrativo(
        self,
        referencia: str,
        texto: str,
        versao: str,
        estudo_gerado: str,
        on_status: Optional[Callable[[str], None]] = None,
    ) -> str:
        """Gera o devocional vivo e narrativo (estilo Café com Deus Pai) com histórias reais de terceiros."""
        prompt_minuto = montar_prompt_minuto(referencia, texto, versao, estudo_gerado)
        
        # Primeira tentativa de geração com instrução específica devocional
        resultado = self._generate(
            prompt=prompt_minuto,
            system_instruction=SYSTEM_PROMPT_DEVOCIONAL,
            on_status=on_status,
        )

        # Validação de integridade: se não contiver textoDevocional com substância, retenta
        if not resultado or len(resultado.strip()) < 200 or "textoDevocional" not in resultado:
            if on_status:
                on_status("⚠️ Devocional narrativo gerado incompleto. Retentando geração com foco estrito...")
            prompt_reforco = (
                f"{prompt_minuto}\n\n"
                "ATENÇÃO CRÍTICA: Responda OBRIGATORIAMENTE em JSON válido com o campo 'textoDevocional' "
                "contendo os 4 parágrafos completos da história e aplicação."
            )
            resultado = self._generate(
                prompt=prompt_reforco,
                system_instruction=SYSTEM_PROMPT_DEVOCIONAL,
                on_status=on_status,
            )

        return resultado
