/**
 * PROJETO BÍBLIA & TEOLOGIA EXPOSITIVA - INTERFACE WEB LOCAL & ONLINE
 * Lógica de apresentação, histórico de estudos, navegação, áudio TTS e temas.
 */

// Estado global da aplicação
let listaEstudos = [];
let currentIndex = 0;
let narradorAudioHandler = null;

document.addEventListener("DOMContentLoaded", () => {
    // 1. Carregamento dos dados (Histórico ou Estudo Único)
    if (typeof HISTORICO_ESTUDOS !== "undefined" && Array.isArray(HISTORICO_ESTUDOS) && HISTORICO_ESTUDOS.length > 0) {
        listaEstudos = HISTORICO_ESTUDOS;
    } else if (typeof ESTUDO_ATUAL !== "undefined") {
        listaEstudos = [ESTUDO_ATUAL];
    } else {
        console.error("Nenhum dado de estudo encontrado. Certifique-se de que data.js está carregado.");
        showToast("⚠️ Não foi possível carregar os dados dos estudos bíblicos.", "error");
        return;
    }

    // 2. Verifica se a URL possui um hash para carregar data específica (ex.: #data-2026-09-29)
    determinarEstudoInicialPorHash();

    // 3. Renderiza estudo ativo e inicializa componentes
    renderizarEstudoAtivo();
    inicializarNavegadorDeEstudos();
    inicializarGavetaHistorico();
    inicializarTema();
    inicializarZenMode();
    inicializarCopiaWhatsApp();
    inicializarAudioNarrador();
    inicializarMeditacaoInterativa();
});

/**
 * Determina o índice do estudo a partir da URL hash se presente.
 */
function determinarEstudoInicialPorHash() {
    const hash = window.location.hash.replace("#", "").replace("data-", "").trim();
    if (hash) {
        const indexEncontrado = listaEstudos.findIndex(e => e.data === hash);
        if (indexEncontrado !== -1) {
            currentIndex = indexEncontrado;
            return;
        }
    }
    currentIndex = 0; // Mais recente por padrão
}

/**
 * Renderiza o estudo correspondente ao índice atual com fidelidade total e dinamismo exegético.
 */
function renderizarEstudoAtivo() {
    const data = listaEstudos[currentIndex];
    if (!data) return;

    // Badges do Topo
    const elData = document.getElementById("meta-data");
    const elVersao = document.getElementById("meta-versao");
    const elGenero = document.getElementById("meta-genero");
    const elModelo = document.getElementById("meta-modelo");

    if (elData) elData.textContent = data.dataFormatada || data.data;
    if (elVersao) elVersao.textContent = data.versao || "NVI";
    if (elGenero) elGenero.textContent = data.genero || "Literatura Bíblica";
    if (elModelo) elModelo.textContent = data.modelo ? `Modelo: ${data.modelo}` : "Gemini 3.5 Flash";

    // Hero: Versículo Principal
    const elVerseText = document.getElementById("verse-text");
    const elVerseRef = document.getElementById("verse-ref");

    if (elVerseText) elVerseText.textContent = data.versiculoTexto;
    if (elVerseRef) elVerseRef.textContent = data.referencia;

    // Seção 01: Contexto Histórico
    const secaoContexto = data.secoes.find(s => s.id === "contexto");
    const elContexto = document.getElementById("conteudo-contexto");
    if (secaoContexto && elContexto) {
        elContexto.innerHTML = formatarMarkdownEditorial(secaoContexto.conteudo);
    }

    // Seção 02: Anatomia do Texto & Termos Originais
    const secaoAnatomia = data.secoes.find(s => s.id === "anatomia");
    const elTermosGrid = document.getElementById("termos-grid");
    const elComparacao = document.getElementById("comparacao-container");
    const elConteudoAnatomia = document.getElementById("conteudo-anatomia");

    if (secaoAnatomia) {
        // Termos Originais no Hebraico/Grego
        if (elTermosGrid) {
            if (Array.isArray(secaoAnatomia.termosOriginais) && secaoAnatomia.termosOriginais.length > 0) {
                elTermosGrid.style.display = "grid";
                elTermosGrid.innerHTML = secaoAnatomia.termosOriginais.map(item => `
                    <div class="term-chip" tabindex="0">
                        <span class="term-name">${escapeHtml(item.termo).replace(/\*/g, "")}</span>
                        <span class="term-meaning">${escapeHtml(item.significado).replace(/\*/g, "")}</span>
                        <span class="term-explanation">${escapeHtml(item.explicacao).replace(/\*/g, "")}</span>
                    </div>
                `).join("");
            } else {
                elTermosGrid.style.display = "none";
                elTermosGrid.innerHTML = "";
            }
        }

        // Caixa de Comparação Exegética de Versões (Ciano/Safira Celestial)
        if (elComparacao) {
            if (data.comparacaoTraducoes) {
                const comp = data.comparacaoTraducoes;
                elComparacao.style.display = "block";
                elComparacao.innerHTML = `
                    <div class="translation-comparison-card">
                        <div class="comparison-card-header">
                            <div class="comparison-header-badge">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                                </svg>
                                <span>${escapeHtml(comp.titulo || "Comparação Exegética de Versões")}</span>
                            </div>
                        </div>

                        <div class="comparison-grid">
                            <!-- Coluna NVI -->
                            <div class="comparison-column col-nvi">
                                <div class="col-header">
                                    <span class="version-tag">${escapeHtml(comp.versaoPrincipal.sigla)}</span>
                                    <span class="emphasis-tag">${escapeHtml(comp.versaoPrincipal.rotulo)}</span>
                                </div>
                                <blockquote class="comparison-quote-box">
                                    <p class="comparison-text">“${escapeHtml(comp.versaoPrincipal.texto)}”</p>
                                </blockquote>
                                <div class="comparison-focus-box">
                                    <span class="focus-label">Foco:</span>
                                    <span class="focus-desc">${escapeHtml(comp.versaoPrincipal.foco)}</span>
                                </div>
                            </div>

                            <!-- Divisor Visual VS -->
                            <div class="comparison-divider">
                                <span class="divider-icon">⚡</span>
                                <span class="divider-label">VS</span>
                            </div>

                            <!-- Coluna Original Hebraico / Grego -->
                            <div class="comparison-column col-original">
                                <div class="col-header">
                                    <span class="version-tag original-tag">${escapeHtml(comp.versaoOriginal.sigla)}</span>
                                    <span class="emphasis-tag">${escapeHtml(comp.versaoOriginal.rotulo)}</span>
                                </div>
                                <blockquote class="comparison-quote-box original-quote-box">
                                    <p class="comparison-text original-text">“${escapeHtml(comp.versaoOriginal.texto)}”</p>
                                </blockquote>
                                <div class="comparison-focus-box original-focus-box">
                                    <span class="focus-label">Foco:</span>
                                    <span class="focus-desc">${escapeHtml(comp.versaoOriginal.foco)}</span>
                                </div>
                            </div>
                        </div>

                        ${comp.notaHermeneutica ? `
                            <div class="comparison-synthesis-box">
                                <div class="synthesis-header">
                                    <span class="synthesis-icon">💡</span>
                                    <strong>Chave Hermenêutica & Teologia Bíblica</strong>
                                </div>
                                <p class="synthesis-text">${escapeHtml(comp.notaHermeneutica)}</p>
                            </div>
                        ` : ""}
                    </div>
                `;
            } else {
                elComparacao.style.display = "none";
                elComparacao.innerHTML = "";
            }
        }

        if (elConteudoAnatomia) {
            elConteudoAnatomia.innerHTML = formatarMarkdownEditorial(secaoAnatomia.conteudo);
        }
    }

    // Seção 03: Aplicação Prática
    const secaoAplicacao = data.secoes.find(s => s.id === "aplicacao");
    const elAplicacao = document.getElementById("conteudo-aplicacao");
    if (secaoAplicacao && elAplicacao) {
        elAplicacao.innerHTML = formatarMarkdownEditorial(secaoAplicacao.conteudo);
    }

    // Seção 04: Conexões Canônicas & Cristo
    const secaoCanonicas = data.secoes.find(s => s.id === "canonicas");
    const elConteudoCanonicas = document.getElementById("conteudo-canonicas");
    const elCitacoesContainer = document.getElementById("citacoes-container");
    const elVersiculosRelacionados = document.getElementById("versiculos-relacionados-container");

    if (secaoCanonicas) {
        if (elConteudoCanonicas) {
            elConteudoCanonicas.innerHTML = formatarMarkdownEditorial(secaoCanonicas.conteudo);
        }

        if (elCitacoesContainer) {
            if (Array.isArray(secaoCanonicas.citacoes) && secaoCanonicas.citacoes.length > 0) {
                elCitacoesContainer.style.display = "flex";
                elCitacoesContainer.innerHTML = secaoCanonicas.citacoes.map(citacao => `
                    <blockquote class="theology-quote">
                        <p class="quote-content">“${escapeHtml(citacao.texto).replace(/\*/g, "")}”</p>
                        <div class="quote-author">
                            ${escapeHtml(citacao.autor).replace(/\*/g, "")}
                            ${citacao.obra ? `<span class="quote-work">• ${escapeHtml(citacao.obra).replace(/\*/g, "")}</span>` : ""}
                        </div>
                    </blockquote>
                `).join("");
            } else {
                elCitacoesContainer.style.display = "none";
                elCitacoesContainer.innerHTML = "";
            }
        }

        // Versículos Correlacionados
        if (elVersiculosRelacionados) {
            if (Array.isArray(data.versiculosRelacionados) && data.versiculosRelacionados.length > 0) {
                elVersiculosRelacionados.style.display = "block";
                elVersiculosRelacionados.innerHTML = `
                    <div class="related-verses-section">
                        <div class="related-header">
                            <span class="badge badge-gold">Conexões Escriturísticas</span>
                            <h3 class="related-title">📖 Versículos Correlacionados & Harmonia Bíblica</h3>
                        </div>
                        <div class="related-verses-grid">
                            ${data.versiculosRelacionados.map(v => `
                                <div class="related-verse-card">
                                    <div class="related-verse-header">
                                        <span class="related-verse-pill">
                                            <svg class="icon-tiny" viewBox="0 0 24 24" fill="currentColor">
                                                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                                            </svg>
                                            ${escapeHtml(v.referencia)}
                                        </span>
                                    </div>
                                    <blockquote class="related-verse-quote">“${escapeHtml(v.texto)}”</blockquote>
                                    <p class="related-verse-context">${escapeHtml(v.contexto)}</p>
                                </div>
                            `).join("")}
                        </div>
                    </div>
                `;
            } else {
                elVersiculosRelacionados.style.display = "none";
                elVersiculosRelacionados.innerHTML = "";
            }
        }
    }

    // Seção 05: Pergunta Central para Meditação
    const secaoPergunta = data.secoes.find(s => s.id === "fechamento");
    const elPergunta = document.getElementById("conteudo-pergunta");
    if (secaoPergunta && elPergunta) {
        elPergunta.textContent = (secaoPergunta.pergunta || "").replace(/\*/g, "").trim();
    }

    // Carrega reflexão salva para esta data
    const reflectionTextarea = document.getElementById("reflection-textarea");
    const reflectionStatus = document.getElementById("reflection-saved-status");
    if (reflectionTextarea) {
        const chave = `biblia_reflexao_${data.data}`;
        reflectionTextarea.value = localStorage.getItem(chave) || "";
        if (reflectionStatus) reflectionStatus.textContent = "";
    }

    // Coluna Lateral: Devocional Rápido
    const elDevotionalText = document.getElementById("devotional-text");
    if (elDevotionalText && data.devocionalWhatsApp) {
        elDevotionalText.innerHTML = formatarMarkdownDevocional(data.devocionalWhatsApp);
    }

    // Botão Compartilhar WhatsApp
    const elBtnShareWhatsApp = document.getElementById("btn-share-whatsapp");
    if (elBtnShareWhatsApp && data.devocionalWhatsApp) {
        const textoCodificado = encodeURIComponent(data.devocionalWhatsApp);
        elBtnShareWhatsApp.href = `https://api.whatsapp.com/send?text=${textoCodificado}`;
    }

    // Atualiza controles da barra de navegação
    atualizarBarraNavegacao();

    // Atualiza marcação ativa na gaveta
    atualizarItemAtivoGaveta();

    // Sincroniza áudio narrador com novo estudo
    if (typeof narradorAudioHandler === "function") {
        narradorAudioHandler(data);
    }
}

/**
 * Atualiza botões anterior / próximo e o indicador de estudo ativo.
 */
function atualizarBarraNavegacao() {
    const total = listaEstudos.length;
    const indicador = document.getElementById("nav-study-indicator");
    const btnPrev = document.getElementById("btn-nav-prev");
    const btnNext = document.getElementById("btn-nav-next");

    if (indicador) {
        const dataAtual = listaEstudos[currentIndex];
        indicador.textContent = `${currentIndex + 1} de ${total}`;
        indicador.title = `${dataAtual.referencia} (${dataAtual.dataFormatada || dataAtual.data})`;
    }

    // Lista ordenada decrescente:
    // index 0 = mais recente (Hoje)
    // index total-1 = mais antigo
    // "Anterior" no tempo significa ir para índice maior (+1)
    // "Próximo" no tempo significa voltar para índice menor (-1)
    if (btnPrev) {
        btnPrev.disabled = currentIndex >= total - 1;
    }
    if (btnNext) {
        btnNext.disabled = currentIndex <= 0;
    }
}

/**
 * Inicializa os botões de navegação anterior/próximo.
 */
function inicializarNavegadorDeEstudos() {
    const btnPrev = document.getElementById("btn-nav-prev");
    const btnNext = document.getElementById("btn-nav-next");

    if (btnPrev) {
        btnPrev.addEventListener("click", () => {
            if (currentIndex < listaEstudos.length - 1) {
                irParaEstudo(currentIndex + 1);
            }
        });
    }

    if (btnNext) {
        btnNext.addEventListener("click", () => {
            if (currentIndex > 0) {
                irParaEstudo(currentIndex - 1);
            }
        });
    }
}

/**
 * Transiciona para um estudo por índice com atualização suave.
 */
function irParaEstudo(novoIndex) {
    if (novoIndex < 0 || novoIndex >= listaEstudos.length) return;
    currentIndex = novoIndex;
    const estudo = listaEstudos[currentIndex];

    // Atualiza hash sem causar salto brusco de scroll
    if (history.replaceState) {
        history.replaceState(null, "", `#data-${estudo.data}`);
    }

    renderizarEstudoAtivo();
    window.scrollTo({ top: 0, behavior: "smooth" });
    showToast(`📖 Exibindo estudo de: ${estudo.referencia} (${estudo.dataFormatada || estudo.data})`);
}

/**
 * Inicializa a gaveta lateral de histórico.
 */
function inicializarGavetaHistorico() {
    const btnHistorico = document.getElementById("btn-historico");
    const btnCloseDrawer = document.getElementById("btn-close-drawer");
    const drawer = document.getElementById("historico-drawer");
    const backdrop = document.getElementById("drawer-backdrop");
    const listaContainer = document.getElementById("historico-list");

    if (!drawer || !backdrop) return;

    // Popula a lista de estudos históricos
    if (listaContainer) {
        listaContainer.innerHTML = listaEstudos.map((estudo, idx) => {
            const snippet = estudo.versiculoTexto || "";
            return `
                <button class="history-card ${idx === currentIndex ? "is-active" : ""}" data-index="${idx}" aria-label="Abrir estudo de ${estudo.referencia}">
                    <div class="history-card-header">
                        <span class="history-card-date">${escapeHtml(estudo.dataFormatada || estudo.data)}</span>
                        <span class="badge badge-accent">${escapeHtml(estudo.versao || "NVI")}</span>
                    </div>
                    <div class="history-card-ref">${escapeHtml(estudo.referencia)}</div>
                    <p class="history-card-snippet">“${escapeHtml(snippet)}”</p>
                </button>
            `;
        }).join("");

        // Clique em item do histórico
        listaContainer.querySelectorAll(".history-card").forEach(card => {
            card.addEventListener("click", () => {
                const targetIdx = parseInt(card.getAttribute("data-index"), 10);
                irParaEstudo(targetIdx);
                fecharGaveta();
            });
        });
    }

    function abrirGaveta() {
        drawer.classList.add("is-open");
        backdrop.classList.add("is-open");
        drawer.setAttribute("aria-hidden", "false");
        backdrop.setAttribute("aria-hidden", "false");
    }

    function fecharGaveta() {
        drawer.classList.remove("is-open");
        backdrop.classList.remove("is-open");
        drawer.setAttribute("aria-hidden", "true");
        backdrop.setAttribute("aria-hidden", "true");
    }

    if (btnHistorico) btnHistorico.addEventListener("click", abrirGaveta);
    if (btnCloseDrawer) btnCloseDrawer.addEventListener("click", fecharGaveta);
    if (backdrop) backdrop.addEventListener("click", fecharGaveta);

    // Fechar gaveta com a tecla ESC
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && drawer.classList.contains("is-open")) {
            fecharGaveta();
        }
    });
}

/**
 * Atualiza o destaque visual do card ativo na gaveta de histórico.
 */
function atualizarItemAtivoGaveta() {
    const cards = document.querySelectorAll(".history-card");
    cards.forEach((card, idx) => {
        if (idx === currentIndex) {
            card.classList.add("is-active");
        } else {
            card.classList.remove("is-active");
        }
    });
}

/**
 * Converte Markdown para HTML editorial limpo, eliminando asteriscos soltos
 * e garantindo tipografia legível e estruturada.
 */
function formatarMarkdownEditorial(texto) {
    if (!texto) return "";
    let html = String(texto);

    // 1. Aspas de versículos ou frases bíblicas em itálico: *"texto"*, *“texto”*, <em>"texto"</em> ou <em>“texto”</em>
    html = html.replace(/\*([“"][^”"\n]+[”"])\*/g, '<span class="bible-verse-quote">$1</span>');
    html = html.replace(/<em>([“"][^”"\n]+[”"])<\/em>/g, '<span class="bible-verse-quote">$1</span>');

    // 2. Negrito duplo: **texto** -> <strong>texto</strong>
    html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

    // 3. Itálico simples: *texto* (não precedido ou seguido por outro *)
    html = html.replace(/(?<!\*)\*([^*\n]+)\*(?!\*)/g, "<em>$1</em>");
    html = html.replace(/(?<!_)_([^_\n]+)_(?!_)/g, "<em>$1</em>");

    // 4. Citações em bloco: > texto
    html = html.replace(/^\s*>\s*([^\n<]+)/gm, '<blockquote class="inline-quote">$1</blockquote>');

    // 5. Marcadores de lista: * item ou - item -> <ul class="editorial-list"><li>...</li></ul>
    html = html.replace(/(?:^\s*[*•-]\s+([^\n]+)\n?)+/gm, (match) => {
        const itens = match.split("\n")
            .map(line => line.trim())
            .filter(line => line.length > 0)
            .map(line => `<li>${line.replace(/^[*•-]\s+/, "")}</li>`)
            .join("");
        return `<ul class="editorial-list">${itens}</ul>`;
    });

    // 6. Remove qualquer asterisco cru remanescente
    html = html.replace(/\*/g, "");

    // 7. Enriquecimento de versículos bíblicos citados no texto: negrito e dourado puro (sem formato de botão)
    const BIBLE_BOOKS_PATTERN = '(?:[123]\\s*)?(?:Gênesis|Êxodo|Levítico|Números|Deuteronômio|Josué|Juízes|Rute|[12]\\s*Samuel|[12]\\s*Reis|[12]\\s*Crônicas|Esdras|Neemias|Ester|Jó|Salmos?|Provérbios?|Eclesiastes|Cânticos|Cantares|Isaías|Jeremias|Lamentações|Ezequiel|Daniel|Oseias|Joel|Amós|Obadias|Jonas|Miqueias|Naum|Habacuque|Sofonias|Ageu|Zacarias|Malaquias|Mateus|Marcos|Lucas|João|Atos|Romanos|[12]\\s*Coríntios?|Gálatas|Efésios|Filipenses|Colossenses|[12]\\s*Tessalonicenses|[12]\\s*Timóteo|Tito|Filemom|Hebreus|Tiago|[12]\\s*Pedro|[123]\\s*João|Judas|Apocalipse|Gn|Êx|Lv|Nm|Dt|Js|Jz|Rt|1Sm|2Sm|1Rs|2Rs|1Cr|2Cr|Ed|Ne|Et|Sl|Pv|Ec|Ct|Is|Jr|Lm|Ez|Dn|Os|Jl|Am|Ob|Jn|Mq|Na|Hc|Sf|Ag|Zc|Ml|Mt|Mc|Lc|Jo|At|Rm|1Co|2Co|Gl|Ef|Fp|Cl|1Ts|2Ts|1Tm|2Tm|Tt|Fm|Hb|Tg|1Pe|2Pe|1Jo|2Jo|3Jo|Jd|Ap)\\.?\\s+\\d+[:\\.]\\d+(?:[\\s\\-–—,]\\d+)*';

    // Normaliza qualquer tag pré-existente de versículo eliminando SVGs e botões
    html = html.replace(/<span class="bible-verse-tag">(?:<svg[\s\S]*?<\/svg>)?\s*([^<]+)<\/span>/gi, '<strong class="bible-verse-tag">$1</strong>');

    // Transforma ocorrências dentro de <strong> (ex: <strong>Marcos 7:21-23</strong>)
    html = html.replace(new RegExp(`<strong>(${BIBLE_BOOKS_PATTERN})<\\/strong>`, 'gi'), '<strong class="bible-verse-tag">$1</strong>');

    // Transforma referências soltas que ainda não foram envolvidas por tag (ex: Jeremias 17:9)
    html = html.replace(new RegExp(`(?<!class="bible-verse-tag">)(?<!<strong>)(${BIBLE_BOOKS_PATTERN})(?!<\\/strong>)`, 'gi'), (match, ref, offset, full) => {
        const before = full.slice(Math.max(0, offset - 40), offset);
        if (before.includes('class="bible-verse-tag"')) return match;
        return `<strong class="bible-verse-tag">${ref}</strong>`;
    });

    // 8. Normaliza quebras de linha em parágrafos se não houver tags de bloco
    if (!html.includes("<br>") && !html.includes("<p>")) {
        html = html.split(/\n{2,}/)
            .filter(p => p.trim().length > 0)
            .map(p => `<p>${p.trim()}</p>`)
            .join("");
    } else if (!html.startsWith("<p>") && !html.startsWith("<div") && !html.startsWith("<ul") && !html.startsWith("<blockquote")) {
        html = `<p>${html}</p>`;
    }

    return html;
}

/**
 * Converte marcações simples de WhatsApp (*negrito*, _itálico_) para HTML enriquecido.
 */
function formatarMarkdownDevocional(texto) {
    if (!texto) return "";
    let formatado = escapeHtml(texto);
    formatado = formatado.replace(/\*([^*\n]+)\*/g, "<strong>$1</strong>");
    formatado = formatado.replace(/_([^_\n]+)_/g, "<em>$1</em>");
    formatado = formatado.replace(/\*/g, "");
    return formatado;
}

/**
 * Gerenciamento do Tema (Dark vs. Pergaminho Light) com persistência local.
 */
function inicializarTema() {
    const btnTheme = document.getElementById("btn-theme");
    const STORAGE_KEY = "biblia_expositiva_theme";
    const temaSalvo = localStorage.getItem(STORAGE_KEY) || "dark";

    aplicarTema(temaSalvo);

    if (btnTheme) {
        btnTheme.addEventListener("click", () => {
            const temaAtual = document.documentElement.getAttribute("data-theme") || "dark";
            const novoTema = temaAtual === "dark" ? "light" : "dark";
            aplicarTema(novoTema);
            localStorage.setItem(STORAGE_KEY, novoTema);
            showToast(novoTema === "light" ? "📜 Modo Pergaminho ativado" : "🌙 Modo Escuro ativado");
        });
    }
}

function aplicarTema(tema) {
    document.documentElement.setAttribute("data-theme", tema);
}

/**
 * Modo Zen / Foco para leitura sem distrações.
 */
function inicializarZenMode() {
    const btnZen = document.getElementById("btn-zen");
    if (!btnZen) return;

    btnZen.addEventListener("click", () => {
        const ativado = document.body.classList.toggle("zen-mode");
        const btnText = btnZen.querySelector(".btn-text");

        if (ativado) {
            if (btnText) btnText.textContent = "Sair do Foco";
            btnZen.classList.add("is-active");
            showToast("📖 Modo Foco ativado: leitura imersiva sem distrações");
        } else {
            if (btnText) btnText.textContent = "Modo Foco";
            btnZen.classList.remove("is-active");
            showToast("Voltou à visualização completa");
        }
    });
}

/**
 * Cópia rápida do devocional para a área de transferência com feedback tátil e visual.
 */
function inicializarCopiaWhatsApp() {
    const btnCopy = document.getElementById("btn-copy-devocional");
    if (!btnCopy) return;

    btnCopy.addEventListener("click", async () => {
        const estudo = listaEstudos[currentIndex];
        if (!estudo || !estudo.devocionalWhatsApp) {
            showToast("Texto devocional não disponível para cópia", "error");
            return;
        }

        try {
            await navigator.clipboard.writeText(estudo.devocionalWhatsApp);
            
            const spanTexto = btnCopy.querySelector("span");
            const textoOriginal = spanTexto ? spanTexto.textContent : "Copiar Texto";
            if (spanTexto) spanTexto.textContent = "Copiado!";
            btnCopy.classList.add("btn-success");

            showToast("✅ Devocional copiado com sucesso para o WhatsApp!");

            setTimeout(() => {
                if (spanTexto) spanTexto.textContent = textoOriginal;
                btnCopy.classList.remove("btn-success");
            }, 2500);
        } catch (err) {
            console.error("Falha ao copiar:", err);
            showToast("Selecione o texto manualmente para copiar", "warning");
        }
    });
}

/**
 * Inicializa os botões interativos da Pergunta Central:
 * Cópia rápida da pergunta e Diário Pessoal de Meditação (armazenado no localStorage).
 */
function inicializarMeditacaoInterativa() {
    const btnCopy = document.getElementById("btn-copy-pergunta");
    const btnToggle = document.getElementById("btn-toggle-reflexao");
    const journalBox = document.getElementById("reflection-journal-box");
    const textarea = document.getElementById("reflection-textarea");
    const btnSave = document.getElementById("btn-salvar-reflexao");
    const status = document.getElementById("reflection-saved-status");

    if (btnCopy) {
        btnCopy.addEventListener("click", async () => {
            const elPergunta = document.getElementById("conteudo-pergunta");
            const pergunta = elPergunta ? elPergunta.textContent.trim() : "";
            if (!pergunta) {
                showToast("Nenhuma pergunta disponível para cópia.", "error");
                return;
            }
            try {
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    await navigator.clipboard.writeText(pergunta);
                } else {
                    const temp = document.createElement("textarea");
                    temp.value = pergunta;
                    document.body.appendChild(temp);
                    temp.select();
                    document.execCommand("copy");
                    document.body.removeChild(temp);
                }
                showToast("📋 Pergunta para meditação copiada com sucesso!");
            } catch (err) {
                console.error("Erro ao copiar pergunta:", err);
                showToast("Não foi possível copiar automaticamente a pergunta.", "warning");
            }
        });
    }

    if (btnToggle && journalBox) {
        btnToggle.addEventListener("click", () => {
            const isHidden = journalBox.style.display === "none" || !journalBox.style.display;
            journalBox.style.display = isHidden ? "flex" : "none";
            if (isHidden && textarea) {
                textarea.focus();
            }
        });
    }

    if (btnSave && textarea) {
        btnSave.addEventListener("click", () => {
            const estudo = listaEstudos[currentIndex];
            if (!estudo) return;
            const chave = `biblia_reflexao_${estudo.data}`;
            localStorage.setItem(chave, textarea.value.trim());
            if (status) {
                status.textContent = "✓ Reflexão salva com sucesso!";
                setTimeout(() => {
                    if (status) status.textContent = "";
                }, 3000);
            }
            showToast("💾 Sua reflexão pessoal foi salva com segurança no navegador.");
        });
    }
}

/**
 * Narrador em Voz Alta via Web Speech API com atualização reativa do estudo ativo.
 */
function inicializarAudioNarrador() {
    const btnAudio = document.getElementById("btn-audio");
    if (!btnAudio) return;

    if (!("speechSynthesis" in window)) {
        btnAudio.style.display = "none";
        return;
    }

    let isPlaying = false;
    const synth = window.speechSynthesis;
    let utterance = null;

    function pararAudio() {
        if (synth && synth.speaking) {
            synth.cancel();
        }
        isPlaying = false;
        atualizarBtnAudio(btnAudio, false, "Ouvir");
    }

    // Registra função para parar áudio quando o usuário mudar de estudo
    narradorAudioHandler = () => {
        pararAudio();
    };

    btnAudio.addEventListener("click", () => {
        const estudo = listaEstudos[currentIndex];
        if (!estudo) return;

        if (isPlaying) {
            if (synth.speaking && !synth.paused) {
                synth.pause();
                isPlaying = false;
                atualizarBtnAudio(btnAudio, false, "Continuar");
                showToast("⏸️ Narração pausada");
                return;
            } else if (synth.paused) {
                synth.resume();
                isPlaying = true;
                atualizarBtnAudio(btnAudio, true, "Pausar");
                showToast("▶️ Continuando narração...");
                return;
            }
        }

        synth.cancel();

        const textoNarracao = `
            Versículo do dia. ${estudo.referencia}.
            ${estudo.versiculoTexto}.
            
            Devocional rápido:
            ${limparTextoParaAudio(estudo.devocionalWhatsApp)}
        `.trim();

        utterance = new SpeechSynthesisUtterance(textoNarracao);
        utterance.lang = "pt-BR";
        utterance.rate = 0.95;
        utterance.pitch = 0.98;

        const vozes = synth.getVoices();
        const vozPt = vozes.find(v => v.lang.startsWith("pt") && (v.name.includes("Natural") || v.name.includes("Google") || v.name.includes("Microsoft") || v.name.includes("Luciana") || v.name.includes("Daniel")));
        if (vozPt) {
            utterance.voice = vozPt;
        }

        utterance.onstart = () => {
            isPlaying = true;
            atualizarBtnAudio(btnAudio, true, "Pausar");
            showToast("🔊 Iniciando narração do versículo e devocional...");
        };

        utterance.onend = () => {
            isPlaying = false;
            atualizarBtnAudio(btnAudio, false, "Ouvir");
            showToast("✨ Narração concluída.");
        };

        utterance.onerror = (e) => {
            console.error("Erro na síntese de voz:", e);
            isPlaying = false;
            atualizarBtnAudio(btnAudio, false, "Ouvir");
        };

        synth.speak(utterance);
    });

    window.addEventListener("beforeunload", () => {
        if (synth && synth.speaking) {
            synth.cancel();
        }
    });
}

function atualizarBtnAudio(btn, ativo, label) {
    const spanText = btn.querySelector(".btn-text");
    if (spanText) spanText.textContent = label;
    if (ativo) {
        btn.classList.add("is-narrating");
    } else {
        btn.classList.remove("is-narrating");
    }
}

function limparTextoParaAudio(texto) {
    if (!texto) return "";
    return texto
        .replace(/\*/g, "")
        .replace(/_/g, "")
        .replace(/🔍/g, "Pergunta para meditação: ")
        .replace(/📱/g, "")
        .replace(/📖/g, "")
        .replace(/✝/g, "")
        .trim();
}

/**
 * Sistema de Notificações Toast com animação suave.
 */
function showToast(mensagem, tipo = "info", duracao = 3500) {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `toast toast-${tipo}`;
    toast.textContent = mensagem;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = "toastOut 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards";
        setTimeout(() => {
            if (toast.parentNode === container) {
                container.removeChild(toast);
            }
        }, 300);
    }, duracao);
}

/**
 * Utilitário de segurança para prevenir injeção XSS simples.
 */
function escapeHtml(texto) {
    if (!texto) return "";
    return String(texto)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
