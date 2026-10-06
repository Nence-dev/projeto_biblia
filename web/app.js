/**
 * PROJETO BÍBLIA & TEOLOGIA EXPOSITIVA - INTERFACE WEB LOCAL & ONLINE
 * Lógica de apresentação, histórico de estudos, navegação, áudio TTS e temas.
 */

// Estado global da aplicação
let listaEstudos = [];
let currentIndex = 0;
let narradorAudioHandler = null;

document.addEventListener("DOMContentLoaded", () => {
    // 1. Carregamento dos dados (Garante que o último postado esteja sempre no topo)
    if (typeof HISTORICO_ESTUDOS !== "undefined" && Array.isArray(HISTORICO_ESTUDOS) && HISTORICO_ESTUDOS.length > 0) {
        listaEstudos = [...HISTORICO_ESTUDOS].sort((a, b) => (b.data || "").localeCompare(a.data || ""));
    } else if (typeof ESTUDO_ATUAL !== "undefined") {
        listaEstudos = [ESTUDO_ATUAL];
    } else {
        console.error("Nenhum dado de estudo encontrado. Certifique-se de que data.js está carregado.");
        showToast("⚠️ Não foi possível carregar os dados dos estudos bíblicos.", "error");
        return;
    }

    // 2. Verifica se a URL possui um hash para carregar data específica (ex.: #data-2026-09-29)
    determinarEstudoInicialPorHash();

    // 3. Inicializa abas e ações primeiro para garantir os ouvintes de clique imediatamente
    inicializarNavegacaoAbas();
    inicializarAcoesCafe();
    inicializarLeitorBiblia();

    // 4. Renderiza estudo ativo e inicializa demais componentes
    try {
        renderizarEstudoAtivo();
    } catch (err) {
        console.error("Erro ao renderizar estudo ativo:", err);
    }

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
    currentIndex = 0; // Mais recente por padrão (Versículo do Dia)
}

/**
 * Renderiza o estudo correspondente ao índice atual com fidelidade total e dinamismo exegético.
 */
function renderizarEstudoAtivo() {
    const data = listaEstudos[currentIndex];
    if (!data) return;

    // Sincroniza estado de visualização do hero conforme a aba ativa
    const abaAtiva = localStorage.getItem("biblia_aba_ativa") || "estudo";
    const heroHeader = document.getElementById("hero-header");
    if (abaAtiva === "minuto" || abaAtiva === "cafe") {
        if (heroHeader) heroHeader.style.display = "none";
        document.body.classList.add("is-mode-minuto");
    } else {
        if (heroHeader) heroHeader.style.display = "block";
        document.body.classList.remove("is-mode-minuto");
    }

    // Atualiza o título dinâmico da página
    document.title = `${data.referencia} - Versículo do Dia & Teologia Expositiva`;

    // Breadcrumb Superior
    const elBreadcrumbRef = document.getElementById("breadcrumb-ref");
    if (elBreadcrumbRef) elBreadcrumbRef.textContent = data.referencia;

    // Badges do Topo e Datas Visíveis
    const elData = document.getElementById("meta-data");
    const elVersao = document.getElementById("meta-versao");
    const elGenero = document.getElementById("meta-genero");
    const dataFormatadaTexto = data.dataFormatada || formatarDataPorExtenso(data.data);

    if (elData) elData.textContent = dataFormatadaTexto;
    if (elVersao) elVersao.textContent = data.versao || "NVI";
    if (elGenero) elGenero.textContent = data.genero || "Literatura Bíblica";

    const elHeroDisplayDate = document.getElementById("hero-display-date");
    if (elHeroDisplayDate) elHeroDisplayDate.textContent = dataFormatadaTexto;

    const elBreadcrumbDate = document.getElementById("breadcrumb-date");
    if (elBreadcrumbDate) elBreadcrumbDate.textContent = dataFormatadaTexto;

    // Hero: Versículo Principal com Destaque Dourado
    const elVerseText = document.getElementById("verse-text");
    const elVerseRef = document.getElementById("verse-ref");

    if (elVerseText) {
        const textoOriginal = data.versiculoTexto || "";
        if (textoOriginal.includes("o susterá") || textoOriginal.includes("o sustentará")) {
            elVerseText.innerHTML = escapeHtml(textoOriginal)
                .replace(/(o susterá;?|o sustentará;?)/gi, '<span class="hero-word-accent">$1</span>');
        } else {
            elVerseText.textContent = textoOriginal;
        }
    }
    if (elVerseRef) elVerseRef.textContent = data.referencia;

    // =========================================================================
    // SIDEBAR EDITORIAL (4 CARDS DA REFERÊNCIA VISUAL)
    // =========================================================================
    // Card 1: SOBRE ESTE ESTUDO
    const elSideLivro = document.getElementById("sidebar-meta-livro");
    const elSideCap = document.getElementById("sidebar-meta-cap");
    const elSideTema = document.getElementById("sidebar-meta-tema");
    const elSideTipo = document.getElementById("sidebar-meta-tipo");
    const elSideDuracao = document.getElementById("sidebar-meta-duracao");

    if (data.referencia) {
        const partesRef = data.referencia.split(" ");
        const livroNome = partesRef.length > 1 ? partesRef.slice(0, -1).join(" ") : partesRef[0];
        const capVers = partesRef.length > 1 ? partesRef[partesRef.length - 1] : "";
        if (elSideLivro) elSideLivro.textContent = `Livro de ${livroNome}`;
        if (elSideCap) elSideCap.textContent = capVers ? `Capítulo ${capVers}` : "Texto Canônico";
    }
    if (elSideTema) {
        elSideTema.textContent = data.genero ? data.genero.split("/")[0].trim() : "Confiança em Deus";
    }
    if (elSideTipo) {
        elSideTipo.textContent = "Estudo Expositivo";
    }
    if (elSideDuracao) {
        const palavrasTotais = (data.secoes || []).reduce((acc, s) => {
            return acc + (s.conteudo ? s.conteudo.split(/\s+/).length : 0);
        }, 0);
        const minEstimados = Math.max(5, Math.round(palavrasTotais / 150));
        elSideDuracao.textContent = `Aproximadamente ${minEstimados} min`;
    }

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

        // Caixa de Comparação Exegética de Versões (Sola Scriptura / Ouro Velho)
        if (elComparacao) {
            if (data.comparacaoTraducoes) {
                const comp = data.comparacaoTraducoes;
                const vPrincipal = comp.versaoPrincipal || {};
                const vOriginal = comp.versaoOriginal || comp.versaoLiteral || {};
                const nota = comp.notaHermeneutica || comp.chaveHermeneutica || "";

                elComparacao.style.display = "block";
                elComparacao.innerHTML = `
                    <div class="translation-comparison-card">
                        <div class="comparison-card-header">
                            <div class="comparison-header-badge">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                                </svg>
                                <span>${escapeHtml(comp.titulo || "Comparação Exegética de Versões")}</span>
                            </div>
                        </div>

                        <div class="comparison-grid">
                            <!-- Coluna NVI / Versão Principal -->
                            <div class="comparison-column col-nvi">
                                <div class="col-header">
                                    <span class="version-tag">${escapeHtml(vPrincipal.sigla || "NVI")}</span>
                                    <span class="emphasis-tag">${escapeHtml(vPrincipal.rotulo || "Equivalência Dinâmica")}</span>
                                </div>
                                <blockquote class="comparison-quote-box">
                                    <p class="comparison-text">“${escapeHtml(vPrincipal.texto || data.versiculoTexto || "")}”</p>
                                </blockquote>
                                <div class="comparison-focus-box">
                                    <span class="focus-label">Foco:</span>
                                    <span class="focus-desc">${escapeHtml(vPrincipal.foco || "Clareza contemporânea")}</span>
                                </div>
                            </div>

                            <!-- Divisor Visual VS Clássico -->
                            <div class="comparison-divider" aria-hidden="true">
                                <span class="divider-badge">VS</span>
                            </div>

                            <!-- Coluna Original Hebraico / Grego / Literal -->
                            <div class="comparison-column col-original">
                                <div class="col-header">
                                    <span class="version-tag original-tag">${escapeHtml(vOriginal.sigla || "Tradução Literal")}</span>
                                    <span class="emphasis-tag">${escapeHtml(vOriginal.rotulo || "Formal / Literal")}</span>
                                </div>
                                <blockquote class="comparison-quote-box original-quote-box">
                                    <p class="comparison-text original-text">“${escapeHtml(vOriginal.textoLiteral || vOriginal.texto || "")}”</p>
                                </blockquote>
                                <div class="comparison-focus-box original-focus-box">
                                    <span class="focus-label">Foco:</span>
                                    <span class="focus-desc">${escapeHtml(vOriginal.foco || "Precisão dos termos originais")}</span>
                                </div>
                            </div>
                        </div>

                        ${nota ? `
                            <div class="comparison-synthesis-box">
                                <div class="synthesis-header">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" style="width: 14px; height: 14px; flex-shrink: 0;">
                                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                                    </svg>
                                    <strong>Chave Hermenêutica & Teologia Bíblica</strong>
                                </div>
                                <p class="synthesis-text">${escapeHtml(nota)}</p>
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
    const textoWhatsApp = data.devocionalWhatsApp || data.whatsapp || "";
    if (elDevotionalText && textoWhatsApp) {
        elDevotionalText.innerHTML = formatarMarkdownDevocional(textoWhatsApp);
    }

    // Botão Compartilhar WhatsApp
    const elBtnShareWhatsApp = document.getElementById("btn-share-whatsapp");
    if (elBtnShareWhatsApp && textoWhatsApp) {
        const textoCodificado = encodeURIComponent(textoWhatsApp);
        elBtnShareWhatsApp.href = `https://api.whatsapp.com/send?text=${textoCodificado}`;
    }

    // Atualiza marcação ativa na gaveta
    atualizarItemAtivoGaveta();

    // Renderiza a experiência Café com Deus Pai para esta data
    renderizarConteudoCafe(data);

    // Sincroniza áudio narrador com novo estudo
    if (typeof narradorAudioHandler === "function") {
        narradorAudioHandler(data);
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
 * Sempre ativado por padrão conforme especificação do usuário.
 */
function inicializarZenMode() {
    const btnZen = document.getElementById("btn-zen");

    // Sempre ativa o Modo Foco ao abrir o site
    document.body.classList.add("zen-mode");
    if (btnZen) {
        btnZen.classList.add("is-active");
        const btnText = btnZen.querySelector(".btn-text");
        if (btnText) btnText.textContent = "Sair do Foco";
    }

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

/* ==========================================================================
   SISTEMA DE NAVEGAÇÃO POR ABAS: ESTUDO EXPOSITIVO & CAFÉ COM DEUS PAI
   ========================================================================== */

/**
 * Inicializa a navegação por abas com persistência e acessibilidade ARIA.
 */
function inicializarNavegacaoAbas() {
    const btnEstudo = document.getElementById("tab-btn-estudo");
    const btnCafe = document.getElementById("tab-btn-cafe");
    const btnBiblia = document.getElementById("tab-btn-biblia");

    if (!btnEstudo || !btnCafe) return;

    btnEstudo.addEventListener("click", () => trocarAba("estudo"));
    btnCafe.addEventListener("click", () => trocarAba("cafe"));
    if (btnBiblia) {
        btnBiblia.addEventListener("click", () => trocarAba("biblia"));
    }

    // Clique na Marca para ir ao Topo/Estudo Expositivo
    const brandHome = document.getElementById("brand-home");
    const irParaInicio = (e) => {
        if (e) e.preventDefault();
        trocarAba("estudo");
        window.scrollTo({ top: 0, behavior: "smooth" });
    };
    if (brandHome) brandHome.addEventListener("click", irParaInicio);

    // Botão Versículos Marcados no Menu Superior (abre o Drawer de destaques de qualquer tela)
    const navHighlights = document.getElementById("nav-btn-highlights");
    if (navHighlights) {
        navHighlights.addEventListener("click", (e) => {
            e.preventDefault();
            if (typeof abrirGavetaMarcacoes === "function") {
                abrirGavetaMarcacoes();
            }
        });
    }

    // Busca Rápida na Navbar
    const searchInput = document.getElementById("navbar-search-input");
    if (searchInput) {
        searchInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                const query = searchInput.value.trim().toLowerCase();
                if (!query) return;
                const idx = listaEstudos.findIndex(item => {
                    return (item.referencia && item.referencia.toLowerCase().includes(query)) ||
                           (item.versiculoTexto && item.versiculoTexto.toLowerCase().includes(query)) ||
                           (item.genero && item.genero.toLowerCase().includes(query));
                });
                if (idx !== -1) {
                    irParaEstudo(idx);
                    trocarAba("estudo");
                } else {
                    showToast(`Nenhum estudo encontrado para "${searchInput.value}"`, "warning");
                }
            }
        });
    }

    // Recupera a aba preferida do usuário (ou padrão "estudo")
    const abaSalva = localStorage.getItem("biblia_aba_ativa") || "estudo";
    trocarAba(abaSalva, false);
}

/**
 * Alterna a visualização entre Estudo Expositivo, Devocional e Leitor Bíblico.
 */
function trocarAba(nomeAba, persistir = true) {
    const btnEstudo = document.getElementById("tab-btn-estudo");
    const btnCafe = document.getElementById("tab-btn-cafe") || document.getElementById("tab-btn-minuto");
    const btnBiblia = document.getElementById("tab-btn-biblia");
    const viewEstudo = document.getElementById("view-estudo");
    const viewCafe = document.getElementById("view-cafe") || document.getElementById("view-minuto");
    const viewBiblia = document.getElementById("view-biblia");
    const heroHeader = document.getElementById("hero-header");

    if (!btnEstudo || !btnCafe || !viewEstudo || !viewCafe) return;

    if (nomeAba === "biblia") {
        if (btnBiblia) {
            btnBiblia.classList.add("is-active");
            btnBiblia.setAttribute("aria-selected", "true");
            btnBiblia.setAttribute("tabindex", "0");
        }
        btnEstudo.classList.remove("is-active");
        btnEstudo.setAttribute("aria-selected", "false");
        btnEstudo.setAttribute("tabindex", "-1");

        btnCafe.classList.remove("is-active");
        btnCafe.setAttribute("aria-selected", "false");
        btnCafe.setAttribute("tabindex", "-1");

        if (heroHeader) heroHeader.style.display = "none";
        viewEstudo.style.display = "none";
        viewCafe.style.display = "none";
        if (viewBiblia) viewBiblia.style.display = "block";

        document.body.classList.remove("is-mode-minuto");

        if (typeof carregarCapituloBiblicoAtual === "function") {
            carregarCapituloBiblicoAtual();
        }

        if (persistir) {
            localStorage.setItem("biblia_aba_ativa", "biblia");
            window.scrollTo({ top: 0, behavior: "smooth" });
        }
    } else if (nomeAba === "cafe" || nomeAba === "minuto") {
        btnCafe.classList.add("is-active");
        btnCafe.setAttribute("aria-selected", "true");
        btnCafe.setAttribute("tabindex", "0");

        btnEstudo.classList.remove("is-active");
        btnEstudo.setAttribute("aria-selected", "false");
        btnEstudo.setAttribute("tabindex", "-1");

        if (btnBiblia) {
            btnBiblia.classList.remove("is-active");
            btnBiblia.setAttribute("aria-selected", "false");
            btnBiblia.setAttribute("tabindex", "-1");
        }

        if (heroHeader) heroHeader.style.display = "none";
        viewEstudo.style.display = "none";
        if (viewBiblia) viewBiblia.style.display = "none";
        viewCafe.style.display = "block";

        document.body.classList.add("is-mode-minuto");

        if (typeof listaEstudos !== "undefined" && typeof currentIndex !== "undefined" && listaEstudos[currentIndex]) {
            renderizarConteudoMinuto(listaEstudos[currentIndex]);
        }

        if (persistir) {
            localStorage.setItem("biblia_aba_ativa", "minuto");
            window.scrollTo({ top: 0, behavior: "smooth" });
        }
    } else {
        btnEstudo.classList.add("is-active");
        btnEstudo.setAttribute("aria-selected", "true");
        btnEstudo.setAttribute("tabindex", "0");

        btnCafe.classList.remove("is-active");
        btnCafe.setAttribute("aria-selected", "false");
        btnCafe.setAttribute("tabindex", "-1");

        if (btnBiblia) {
            btnBiblia.classList.remove("is-active");
            btnBiblia.setAttribute("aria-selected", "false");
            btnBiblia.setAttribute("tabindex", "-1");
        }

        if (heroHeader) heroHeader.style.display = "block";
        viewCafe.style.display = "none";
        if (viewBiblia) viewBiblia.style.display = "none";
        viewEstudo.style.display = "block";

        document.body.classList.remove("is-mode-minuto");

        if (persistir) {
            localStorage.setItem("biblia_aba_ativa", "estudo");
            window.scrollTo({ top: 0, behavior: "smooth" });
        }
    }
}

/**
 * Calcula dinamicamente o número do dia no ano (ex: 279/365).
 */
function calcularDiaDoAno(dataStr) {
    if (!dataStr) return "279/365";
    const partes = dataStr.split("-");
    if (partes.length < 3) return "279/365";
    const ano = parseInt(partes[0], 10);
    const mes = parseInt(partes[1], 10) - 1;
    const dia = parseInt(partes[2], 10);

    const dataAlvo = new Date(ano, mes, dia);
    const inicioAno = new Date(ano, 0, 1);
    const diferencaMs = dataAlvo - inicioAno;
    const umDiaMs = 1000 * 60 * 60 * 24;
    const diaNum = Math.floor(diferencaMs / umDiaMs) + 1;
    const totalDias = (ano % 4 === 0 && (ano % 100 !== 0 || ano % 400 === 0)) ? 366 : 365;

    return `${String(diaNum).padStart(2, "0")}/${totalDias}`;
}

/**
 * Formata a data no formato por extenso: "6 de Outubro de 2026".
 */
function formatarDataPorExtenso(dataStr) {
    if (!dataStr) return "";
    const partes = dataStr.split("-");
    if (partes.length < 3) return dataStr;
    const dia = parseInt(partes[2], 10);
    const meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
    const mesIdx = parseInt(partes[1], 10) - 1;
    const mesStr = meses[mesIdx] || "";
    const ano = partes[0];
    return `${dia} de ${mesStr} de ${ano}`;
}

/**
 * Formata a data no estilo compacto editorial: 06 | OUT.
 */
function formatarDataCompacta(dataStr) {
    if (!dataStr) return "06 | OUT";
    const partes = dataStr.split("-");
    if (partes.length < 3) return "06 | OUT";
    const dia = partes[2].padStart(2, "0");
    const meses = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"];
    const mesIdx = parseInt(partes[1], 10) - 1;
    const mesStr = meses[mesIdx] || "OUT";
    return `${dia} | ${mesStr}`;
}

/**
 * Recupera ou sintetiza com excelência os dados editoriais da folha Minuto com Deus.
 */
function obterDadosMinutoComFallback(data) {
    const versiculoRef = data.referencia || "A Palavra de Deus";
    const textoVersiculo = data.versiculoTexto || data.versiculo || "";
    const diaDoAnoCalc = calcularDiaDoAno(data.data);
    const dataCompactaCalc = formatarDataCompacta(data.data);

    // Mapeamento contextual inteligente por livro / versículo / palavras-chave
    const refUpper = (versiculoRef || "").toUpperCase();
    const vUpper = (textoVersiculo || "").toUpperCase();

    let tituloCtx = "DESCANSO NA PALAVRA";
    let fraseCtx = "A Palavra de Deus não é um manual de regras frias, é o alicerce vivo para a sua alma hoje.";
    let autorCtx = "@cslewis";
    let leiturasCtx = ["SALMOS 119.105", "2 TIMÓTEO 3.16,17", "HEBREUS 4.12", "TIAGO 1.22"];
    let leituraPrincipalCtx = "SALMOS 119.105";

    if (refUpper.includes("55:22") || vUpper.includes("SUSTER") || vUpper.includes("FARDO") || vUpper.includes("PREOCUPAÇ")) {
        tituloCtx = "SUSTENTO INABALÁVEL";
        fraseCtx = "Você não foi desenhado para carregar o peso do mundo sozinho; entregue o fardo a Quem sustenta o universo.";
        autorCtx = "@cslewis";
        leiturasCtx = ["1 PEDRO 5.7", "MATEUS 11.28-30", "SALMOS 68.19", "FILIPENSES 4.6,7", "ISAÍAS 41.10"];
        leituraPrincipalCtx = "1 PEDRO 5.7";
    } else if (refUpper.includes("JUDAS") || vUpper.includes("DUVID") || vUpper.includes("MISERICÓRDIA")) {
        tituloCtx = "O ABRIGO DA MISERICÓRDIA";
        fraseCtx = "A misericórdia não descarta quem está vacilando; ela estende a mão para curar.";
        autorCtx = "@timkeller";
        leiturasCtx = ["LUCAS 15.11-24", "MATEUS 12.20", "ROMANOS 14.1", "GÁLATAS 6.1,2", "1 TESSALONICENSES 5.14"];
        leituraPrincipalCtx = "LUCAS 15.11-24";
    } else if (refUpper.includes("51:10") || vUpper.includes("CORAÇÃO PURO") || vUpper.includes("PURIFIC")) {
        tituloCtx = "A PUREZA DO CORAÇÃO";
        fraseCtx = "Deus não reforma nossa fachada moral; Ele recria o coração a partir do arrependimento sincero.";
        autorCtx = "@agostinho";
        leiturasCtx = ["EZEQUIEL 36.26", "MATEUS 5.8", "1 JOÃO 1.9", "SALMOS 24.3,4", "TITO 3.5"];
        leituraPrincipalCtx = "EZEQUIEL 36.26";
    } else if (refUpper.includes("4:23") || vUpper.includes("PENSAMENTO") || vUpper.includes("GUARDA")) {
        tituloCtx = "A GUARDA DO CORAÇÃO";
        fraseCtx = "Vigiar o coração não é viver em paranoia; é proteger a nascente pura para que a vida não adoeça.";
        autorCtx = "@agostinho";
        leiturasCtx = ["FILIPENSES 4.8", "ROMANOS 12.2", "LUCAS 6.45", "COLOSSENSES 3.2", "SALMOS 139.23,24"];
        leituraPrincipalCtx = "FILIPENSES 4.8";
    } else if (refUpper.includes("8:1") || vUpper.includes("CONDENA")) {
        tituloCtx = "LIVRES DA CONDENAÇÃO";
        fraseCtx = "A cruz liquidou a sentença penal: quem está em Cristo não deve nada ao tribunal da culpa.";
        autorCtx = "@johnstott";
        leiturasCtx = ["JOÃO 5.24", "ISAÍAS 53.5", "ROMANOS 5.1", "COLOSSENSES 2.14", "HEBREUS 10.14"];
        leituraPrincipalCtx = "JOÃO 5.24";
    } else if (refUpper.includes("7:37") || vUpper.includes("SEDE") || vUpper.includes("ÁGUA VIVA")) {
        tituloCtx = "INESGOTÁVEL";
        fraseCtx = "Só Deus pode satisfazer o anseio mais íntimo da sua alma.";
        autorCtx = "@juniorrostirola";
        leiturasCtx = ["APOCALIPSE 22.17", "JEREMIAS 2.13", "SALMOS 36.9", "JOÃO 4.13,14", "ISAÍAS 55.1", "ISAÍAS 44.3"];
        leituraPrincipalCtx = "JOÃO 4.13,14";
    } else if (refUpper.includes("APOCALIPSE 2") || vUpper.includes("PRIMEIRO AMOR")) {
        tituloCtx = "DE VOLTA AO PRIMEIRO AMOR";
        fraseCtx = "Lembre-se de onde você caiu e volte ao primeiro amor.";
        autorCtx = "@juniorrostirola";
        leiturasCtx = ["JEREMIAS 2.2", "MATEUS 24.12", "HEBREUS 10.32-36", "GÁLATAS 6.9", "HEBREUS 6.10-12", "JOÃO 21.15-17"];
        leituraPrincipalCtx = "JEREMIAS 2.2";
    }

    if (data.minutoComDeus && typeof data.minutoComDeus === "object") {
        const tituloSalvo = data.minutoComDeus.titulo;
        const tituloFinal = (!tituloSalvo || tituloSalvo === "NOVOS COMEÇOS") ? tituloCtx : tituloSalvo;

        let leiturasFinais = data.minutoComDeus.leiturasComplementares;
        if (!leiturasFinais || !Array.isArray(leiturasFinais) || leiturasFinais.length === 0) {
            if (data.minutoComDeus.leituraComplementar && data.minutoComDeus.leituraComplementar !== "1 PEDRO 5.6-11") {
                leiturasFinais = [data.minutoComDeus.leituraComplementar];
            } else {
                leiturasFinais = leiturasCtx;
            }
        }

        return {
            titulo: tituloFinal,
            dataCompacta: data.minutoComDeus.dataCompacta || dataCompactaCalc,
            diaDoAno: data.minutoComDeus.diaDoAno || diaDoAnoCalc,
            fraseDoDia: data.minutoComDeus.fraseDoDia || fraseCtx,
            autorFrase: data.minutoComDeus.autorFrase || autorCtx,
            leiturasComplementares: leiturasFinais,
            leituraComplementar: data.minutoComDeus.leituraComplementar || leiturasFinais[0] || leituraPrincipalCtx,
            textoDevocional: data.minutoComDeus.textoDevocional || ""
        };
    }

    const textoProsa = `Todo ser humano tem uma carga máxima de ruptura. Há dias em que a soma das cobranças, dos prazos e das decepções faz a nossa estrutura parecer prestes a desmoronar. A cultura nos ensina a fingir invulnerabilidade, e o ambiente religioso muitas vezes cobra sorrisos artificiais. Mas Davi, ao escrever ${versiculoRef} debaixo da dor aguda de uma traição, tomou uma decisão cirúrgica: ele não fingiu força; ele arremessou o peso nos braços de Deus.\n\nO Senhor nos lembra através da Sua Palavra: "${textoVersiculo}". A promessa divina não é de mágica instantânea, mas de sustento estrutural contínuo. Ele não prometeu a ausência de atrito no mundo, mas garantiu ser a coluna inabalável que impede a sua vida de entrar em colapso.\n\nTalvez hoje você tenha acordado com o peito apertado, tentando calcular como resolver tudo na força do próprio braço. O Pai está convidando você a dar um basta na ilusão do controle. Faça o seu melhor com seriedade, mas respire fundo e entregue o resultado a Quem tem ombros infinitamente largos para sustentar a sua caminhada.`;

    return {
        titulo: tituloCtx,
        dataCompacta: dataCompactaCalc,
        diaDoAno: diaDoAnoCalc,
        fraseDoDia: fraseCtx,
        autorFrase: autorCtx,
        leiturasComplementares: leiturasCtx,
        leituraComplementar: leituraPrincipalCtx,
        textoDevocional: textoProsa
    };
}

/**
 * Renderiza o devocional no formato da nova imagem de referência (Lanterna, Bússola e Relógio, Salmos).
 */
function renderizarConteudoMinuto(data) {
    if (!data) return;

    const minutoData = obterDadosMinutoComFallback(data);

    // 1. Hero Devocional Banner: Data Compacta, Título e Versículo
    const elHeroDate = document.getElementById("devocional-date-text") || document.getElementById("minuto-data-compacta");
    if (elHeroDate) elHeroDate.textContent = minutoData.dataCompacta;

    const elHeroTitle = document.getElementById("devocional-hero-title") || document.getElementById("minuto-titulo-devocional");
    if (elHeroTitle) elHeroTitle.textContent = minutoData.titulo.toUpperCase();

    const elHeroVerse = document.getElementById("devocional-hero-verse") || document.getElementById("minuto-versiculo-texto");
    if (elHeroVerse) {
        const vTexto = data.versiculoTexto || data.versiculo || "";
        elHeroVerse.textContent = vTexto ? `“${vTexto}”` : "";
    }

    const elHeroRef = document.getElementById("devocional-hero-ref");
    if (elHeroRef) {
        elHeroRef.innerHTML = `<span class="cross-icon" aria-hidden="true">†</span> <span>${(data.referencia || "").toUpperCase()}</span>`;
    }

    // 2. Sidebar Esquerda: Card com Bússola & Relógio, Frase, Progresso e Leituras
    const elFraseDia = document.getElementById("devocional-frase-impacto") || document.getElementById("minuto-frase-dia");
    if (elFraseDia) elFraseDia.textContent = `“${minutoData.fraseDoDia}”`;

    const elFraseAutor = document.getElementById("devocional-frase-autor") || document.getElementById("minuto-frase-autor");
    if (elFraseAutor) elFraseAutor.textContent = minutoData.autorFrase;

    const elCounterText = document.getElementById("devocional-counter-text") || document.getElementById("minuto-dia-ano");
    if (elCounterText) elCounterText.textContent = minutoData.diaDoAno;

    // Barra de progresso proporcional
    const elProgressFill = document.getElementById("devocional-progress-fill");
    if (elProgressFill && minutoData.diaDoAno) {
        const partes = minutoData.diaDoAno.split("/");
        if (partes.length === 2) {
            const atual = parseFloat(partes[0]) || 279;
            const total = parseFloat(partes[1]) || 365;
            const pct = Math.min(100, Math.max(1, ((atual / total) * 100))).toFixed(1);
            elProgressFill.style.width = `${pct}%`;
        }
    }

    // Leituras Bíblicas da Sidebar (Lista com 5 passagens)
    const elReadingsList = document.getElementById("devocional-readings-list");
    if (elReadingsList) {
        let leituras = [
            { label: "1 Pedro 5:7", book: "1pedro", cap: 5 },
            { label: "Mateus 11:28-30", book: "mateus", cap: 11 },
            { label: "Filipenses 4:6-7", book: "filipenses", cap: 4 },
            { label: "Salmos 37:5", book: "salmos", cap: 37 },
            { label: "Isaías 41:10", book: "isaias", cap: 41 }
        ];

        if (Array.isArray(minutoData.leiturasComplementares) && minutoData.leiturasComplementares.length > 0) {
            leituras = minutoData.leiturasComplementares.map(ref => {
                const parts = ref.split(" ");
                const bookName = parts[0].toLowerCase().replace(/\./g, "");
                const cap = parseInt(parts[1], 10) || 1;
                return { label: ref, book: bookName, cap };
            });
        }

        elReadingsList.innerHTML = leituras.map(item => `
            <li>
                <a href="#biblia" class="reading-link" data-book="${escapeHtml(item.book)}" data-cap="${item.cap}">
                    ${escapeHtml(item.label)}
                </a>
            </li>
        `).join("");

        // Conecta cada link da lista de leituras para abrir direto no Leitor Bíblico
        elReadingsList.querySelectorAll(".reading-link").forEach(link => {
            link.addEventListener("click", (e) => {
                e.preventDefault();
                const book = link.getAttribute("data-book") || "salmos";
                const cap = parseInt(link.getAttribute("data-cap"), 10) || 1;
                abrirPassagemNaBiblia(book, cap);
            });
        });
    }

    // 3. Anotações Pessoais: Recupera do localStorage
    const textareaNotes = document.getElementById("minuto-notes-textarea") || document.getElementById("cafe-journal-textarea");
    const statusNotes = document.getElementById("minuto-notes-status") || document.getElementById("cafe-journal-status");
    if (textareaNotes) {
        const chaveNotes = `biblia_minuto_notes_${data.data}`;
        textareaNotes.value = localStorage.getItem(chaveNotes) || localStorage.getItem(`biblia_cafe_journal_${data.data}`) || "";
        if (statusNotes) statusNotes.textContent = "";
    }

    // 4. Coluna Principal: Título, Card de Versículo com Borda Dourada e Prosa
    const elMainTitle = document.getElementById("devocional-main-title");
    if (elMainTitle) elMainTitle.textContent = minutoData.titulo;

    const elDevocionalMainDate = document.getElementById("devocional-main-date");
    if (elDevocionalMainDate) {
        elDevocionalMainDate.textContent = data.dataFormatada || formatarDataPorExtenso(data.data);
    }

    const elAccentVerse = document.getElementById("devocional-accent-verse");
    if (elAccentVerse) {
        const vTexto = data.versiculoTexto || data.versiculo || "";
        elAccentVerse.textContent = vTexto ? `“${vTexto}”` : "";
    }

    const elAccentRef = document.getElementById("devocional-accent-ref");
    if (elAccentRef) elAccentRef.textContent = (data.referencia || "").toUpperCase();

    // Prosa Devocional com Letra Capitular (Drop Cap)
    const elStoryProse = document.getElementById("minuto-story-prose");
    if (elStoryProse) {
        const textoCompleto = minutoData.textoDevocional || "";
        const paragrafos = textoCompleto
            .split(/<br\s*\/?>\s*<br\s*\/?>|\n{2,}/)
            .map(p => p.trim())
            .filter(p => p.length > 0);

        if (paragrafos.length > 0) {
            elStoryProse.innerHTML = paragrafos.map((p, idx) => {
                let htmlP = p.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
                             .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>')
                             .replace(/_([^_]+)_/g, '<em>$1</em>');
                if (idx === 0) {
                    const textoLimpo = htmlP.replace(/<[^>]+>/g, "");
                    const primeiraLetra = textoLimpo.charAt(0);
                    const idxPrimeira = htmlP.indexOf(primeiraLetra);
                    if (idxPrimeira !== -1) {
                        const antes = htmlP.slice(0, idxPrimeira);
                        const depois = htmlP.slice(idxPrimeira + 1);
                        return `
                            <p class="devocional-first-p">
                                ${antes}<span class="devocional-drop-cap">${primeiraLetra}</span>${depois}
                            </p>
                        `;
                    }
                }
                return `<p>${htmlP}</p>`;
            }).join("");
        } else {
            elStoryProse.innerHTML = "<p>Momento devocional sendo preparado com carinho.</p>";
        }
    }

    // 5. Atualiza Link Direto do WhatsApp
    const btnShareWhatsapp = document.getElementById("btn-share-whatsapp-minuto") || document.getElementById("btn-share-whatsapp-cafe");
    if (btnShareWhatsapp) {
        const textoZap = gerarTextoCompartilhamentoMinuto(data, minutoData);
        btnShareWhatsapp.href = `https://api.whatsapp.com/send?text=${encodeURIComponent(textoZap)}`;
    }

    // 6. Atualiza Barra de Navegação Inferior (Anterior / Próximo Devocional)
    atualizarNavegacaoInferiorDevocional();
}

/**
 * Atualiza a barra de navegação inferior do devocional com as datas reais:
 * Anterior: Data do dia anterior
 * Próximo: Data do próximo dia (ou 'Aguardar amanhã' se for o dia de hoje)
 */
function atualizarNavegacaoInferiorDevocional() {
    const btnPrev = document.getElementById("btn-devocional-prev");
    const btnNext = document.getElementById("btn-devocional-next");

    if (!btnPrev || !btnNext) return;

    // 1. Botão Anterior (Dia passado / mais antigo na lista decrescente: currentIndex + 1)
    const indexAnterior = currentIndex + 1;
    if (indexAnterior < listaEstudos.length) {
        const estudoAnterior = listaEstudos[indexAnterior];
        const dataFormatada = estudoAnterior.dataFormatada || formatarDataPorExtenso(estudoAnterior.data);
        btnPrev.disabled = false;
        btnPrev.classList.remove("is-disabled");
        btnPrev.setAttribute("aria-disabled", "false");
        btnPrev.innerHTML = `
            <span class="nav-chevron" aria-hidden="true">‹</span>
            <span class="nav-label">Anterior: <strong>${escapeHtml(dataFormatada)}</strong></span>
        `;
        btnPrev.onclick = (e) => {
            if (e) e.preventDefault();
            irParaEstudo(indexAnterior);
            trocarAba("cafe");
            window.scrollTo({ top: 0, behavior: "smooth" });
        };
    } else {
        btnPrev.disabled = true;
        btnPrev.classList.add("is-disabled");
        btnPrev.setAttribute("aria-disabled", "true");
        btnPrev.innerHTML = `
            <span class="nav-chevron" aria-hidden="true">‹</span>
            <span class="nav-label">Anterior: <em>Início do acervo</em></span>
        `;
        btnPrev.onclick = null;
    }

    // 2. Botão Próximo (Dia futuro / mais recente: currentIndex - 1)
    const indexProximo = currentIndex - 1;
    if (indexProximo >= 0) {
        const estudoProximo = listaEstudos[indexProximo];
        const dataFormatada = estudoProximo.dataFormatada || formatarDataPorExtenso(estudoProximo.data);
        btnNext.disabled = false;
        btnNext.classList.remove("is-disabled", "is-waiting");
        btnNext.setAttribute("aria-disabled", "false");
        btnNext.innerHTML = `
            <span class="nav-label">Próximo: <strong>${escapeHtml(dataFormatada)}</strong></span>
            <span class="nav-chevron" aria-hidden="true">›</span>
        `;
        btnNext.onclick = (e) => {
            if (e) e.preventDefault();
            irParaEstudo(indexProximo);
            trocarAba("cafe");
            window.scrollTo({ top: 0, behavior: "smooth" });
        };
    } else {
        // Estamos no estudo mais recente publicado (Hoje)
        btnNext.disabled = false; // Permite toque no mobile para ler o aviso
        btnNext.classList.remove("is-disabled");
        btnNext.classList.add("is-waiting");
        btnNext.setAttribute("aria-disabled", "false");
        btnNext.innerHTML = `
            <span class="nav-label">Próximo: <strong>Aguardar amanhã</strong></span>
            <span class="nav-chevron" aria-hidden="true">›</span>
        `;
        btnNext.onclick = (e) => {
            if (e) e.preventDefault();
            showToast("⏳ O devocional de amanhã será publicado às 05:23!", "info");
        };
    }
}

/**
 * Função de retrocompatibilidade para garantir que qualquer chamada legada funcione perfeitamente.
 */
function renderizarConteudoCafe(data) {
    renderizarConteudoMinuto(data);
}

/**
 * Formata a mensagem completa de Devocional para cópia ou WhatsApp.
 */
function gerarTextoCompartilhamentoMinuto(data, minutoData) {
    const vTexto = data.versiculoTexto || data.versiculo || "";
    const leiturasFormatadas = Array.isArray(minutoData.leiturasComplementares)
        ? minutoData.leiturasComplementares.join(" • ")
        : (minutoData.leituraComplementar || "");

    return `⏱️ *DEVOCIONAL DIÁRIO* | ${minutoData.titulo}\n` +
           `📅 *${minutoData.dataCompacta}* • Devocional ${minutoData.diaDoAno}\n\n` +
           `📖 *Versículo Chave:*\n"${vTexto}"\n— *${data.referencia}*\n\n` +
           `💡 *Reflexão:*\n"${minutoData.fraseDoDia}" (${minutoData.autorFrase})\n\n` +
           `✝️ *Leitura Bíblica:*\n${leiturasFormatadas}\n\n` +
           `🕊️ *Estudo:*\n${minutoData.textoDevocional}\n\n` +
           `✨ Sola Scriptura • Que o Senhor sustente a sua caminhada hoje!`;
}

/**
 * Inicializa interações e botões da aba Devocionais.
 */
function inicializarAcoesMinuto() {
    // Botão Copiar Mensagem
    const btnCopiar = document.getElementById("btn-copy-minuto") || document.getElementById("btn-copy-cafe");
    if (btnCopiar) {
        btnCopiar.addEventListener("click", () => {
            const data = listaEstudos[currentIndex];
            if (!data) return;
            const minutoData = obterDadosMinutoComFallback(data);
            const textoCompleto = gerarTextoCompartilhamentoMinuto(data, minutoData);

            navigator.clipboard.writeText(textoCompleto)
                .then(() => {
                    showToast("Devocional copiado com formatação para a área de transferência!", "success");
                })
                .catch(() => {
                    showToast("Não foi possível copiar automaticamente.", "error");
                });
        });
    }

    // Botão Salvar Anotações Pessoais
    const btnSalvar = document.getElementById("btn-save-minuto-notes") || document.getElementById("btn-save-cafe-journal");
    const textareaNotes = document.getElementById("minuto-notes-textarea") || document.getElementById("cafe-journal-textarea");
    const statusNotes = document.getElementById("minuto-notes-status") || document.getElementById("cafe-journal-status");

    if (btnSalvar && textareaNotes) {
        btnSalvar.addEventListener("click", () => {
            const data = listaEstudos[currentIndex];
            if (!data) return;
            const chave = `biblia_minuto_notes_${data.data}`;
            localStorage.setItem(chave, textareaNotes.value);

            if (statusNotes) {
                statusNotes.textContent = "✓ Anotação salva com sucesso!";
                setTimeout(() => {
                    statusNotes.textContent = "";
                }, 3500);
            }
            showToast("Sua anotação pessoal foi gravada neste dispositivo.", "success");
        });
    }

    // Botão Refletir sobre isso (Scroll suave para Anotações)
    const btnReflect = document.getElementById("btn-devocional-reflect");
    if (btnReflect) {
        btnReflect.addEventListener("click", () => {
            if (textareaNotes) {
                textareaNotes.scrollIntoView({ behavior: "smooth", block: "center" });
                textareaNotes.focus();
                showToast("Escreva sua reflexão no card de Anotações ao lado.", "info");
            }
        });
    }

    // Botão Um Minuto Diário (Oração de Ancoragem)
    const btnMinutePrayer = document.getElementById("btn-start-minute-prayer");
    if (btnMinutePrayer) {
        btnMinutePrayer.addEventListener("click", () => {
            showToast("⏱️ Iniciando 1 minuto de silêncio e oração na presença de Deus...", "info");
            btnMinutePrayer.style.transform = "scale(0.92)";
            setTimeout(() => {
                btnMinutePrayer.style.transform = "scale(1)";
            }, 200);

            let segundosRestantes = 60;
            const timer = setInterval(() => {
                segundosRestantes -= 10;
                if (segundosRestantes <= 0) {
                    clearInterval(timer);
                    showToast("✨ Momento concluído. Que o sustento e a paz do Senhor guardem o seu coração hoje!", "success");
                }
            }, 10000);
        });
    }

    // Mini Cards da Seção OUTROS ESTUDOS SOBRE SALMOS
    document.querySelectorAll(".devocional-mini-card").forEach(card => {
        card.addEventListener("click", () => {
            const slug = card.getAttribute("data-slug");
            if (slug === "salmo-23") {
                abrirPassagemNaBiblia("salmos", 23);
            } else if (slug === "salmo-91") {
                abrirPassagemNaBiblia("salmos", 91);
            } else if (slug === "salmo-121") {
                abrirPassagemNaBiblia("salmos", 121);
            }
        });
    });

    // Barra de Navegação Inferior (Anterior / Próximo)
    atualizarNavegacaoInferiorDevocional();
}

/**
 * Retrocompatibilidade para inicialização.
 */
function inicializarAcoesCafe() {
    inicializarAcoesMinuto();
}

/* ==========================================================================
   10. CONTROLADOR DO LEITOR BÍBLICO CANÔNICO (SOLA SCRIPTURA BIBLE READER)
   Navegação por livros (66 livros), capítulos, versões e ajuste de fonte.
   ========================================================================== */

const bibleState = {
    bookId: "salmos",
    chapter: 55,
    version: "NVI",
    zoom: 100
};

/**
 * Inicializa os controles e componentes do Leitor Bíblico.
 */
function inicializarLeitorBiblia() {
    if (typeof BIBLE_BOOKS === "undefined" || !Array.isArray(BIBLE_BOOKS)) {
        console.warn("BIBLE_BOOKS não está carregado. Certifique-se de carregar bible-data.js.");
        return;
    }

    const selectLivro = document.getElementById("bible-select-livro");
    const selectCapitulo = document.getElementById("bible-select-capitulo");
    const btnZoomIn = document.getElementById("btn-bible-zoom-in");
    const btnZoomOut = document.getElementById("btn-bible-zoom-out");
    const btnHighlights = document.getElementById("btn-bible-highlights");
    const btnCloseHighlights = document.getElementById("btn-close-highlights-drawer");
    const backdropHighlights = document.getElementById("drawer-highlights-backdrop");
    const btnPrevCap = document.getElementById("btn-bible-prev-cap");
    const btnNextCap = document.getElementById("btn-bible-next-cap");

    if (!selectLivro || !selectCapitulo) return;

    // 1. Popula Select de Livros com Grupos Canônicos
    preencherSelectLivros(selectLivro);

    // 2. Popula Select de Capítulos para o Livro Inicial
    preencherSelectCapitulos(selectCapitulo, bibleState.bookId, bibleState.chapter);

    // 3. Ouvintes de Evento dos Controles
    selectLivro.addEventListener("change", () => {
        bibleState.bookId = selectLivro.value;
        bibleState.chapter = 1;
        preencherSelectCapitulos(selectCapitulo, bibleState.bookId, 1);
        carregarCapituloBiblicoAtual();
    });

    selectCapitulo.addEventListener("change", () => {
        bibleState.chapter = parseInt(selectCapitulo.value, 10) || 1;
        carregarCapituloBiblicoAtual();
    });

    // 4. Controles de Zoom
    if (btnZoomIn) {
        btnZoomIn.addEventListener("click", () => ajustarZoomBiblia(10));
    }
    if (btnZoomOut) {
        btnZoomOut.addEventListener("click", () => ajustarZoomBiblia(-10));
    }

    // 5. Versículos Marcados (Drawer & Popover)
    if (btnHighlights) {
        btnHighlights.addEventListener("click", abrirGavetaMarcacoes);
    }
    if (btnCloseHighlights) {
        btnCloseHighlights.addEventListener("click", fecharGavetaMarcacoes);
    }
    if (backdropHighlights) {
        backdropHighlights.addEventListener("click", fecharGavetaMarcacoes);
    }

    inicializarPopoverCores();
    inicializarFiltrosMarcacoes();
    atualizarContadorMarcacoes();

    // 6. Paginação Anterior / Próximo Capítulo
    if (btnPrevCap) {
        btnPrevCap.addEventListener("click", () => navegarCapituloBiblico(-1));
    }
    if (btnNextCap) {
        btnNextCap.addEventListener("click", () => navegarCapituloBiblico(1));
    }

    // 7. Ouvinte reativo para atualizar quando o banco integral NVI terminar de carregar
    if (typeof onBibleNviLoaded === "function") {
        onBibleNviLoaded(() => {
            const currentTab = localStorage.getItem("solascriptura_active_tab");
            if (currentTab === "biblia") {
                carregarCapituloBiblicoAtual();
            }
        });
    }

    // Carrega o texto inicial
    carregarCapituloBiblicoAtual();
}

/**
 * Preenche o select de livros agrupando por Antigo e Novo Testamento.
 */
function preencherSelectLivros(selectElement) {
    selectElement.innerHTML = "";

    const groupAT = document.createElement("optgroup");
    groupAT.label = "— Antigo Testamento —";

    const groupNT = document.createElement("optgroup");
    groupNT.label = "— Novo Testamento —";

    BIBLE_BOOKS.forEach(book => {
        const opt = document.createElement("option");
        opt.value = book.id;
        opt.textContent = `${book.nome} (${book.abrev})`;
        if (book.id === bibleState.bookId) {
            opt.selected = true;
        }

        if (book.testamento === "AT") {
            groupAT.appendChild(opt);
        } else {
            groupNT.appendChild(opt);
        }
    });

    selectElement.appendChild(groupAT);
    selectElement.appendChild(groupNT);
}

/**
 * Preenche o select de capítulos para o livro selecionado.
 */
function preencherSelectCapitulos(selectElement, bookId, capSelecionado = 1) {
    selectElement.innerHTML = "";
    const book = BIBLE_BOOKS.find(b => b.id === bookId);
    if (!book) return;

    for (let c = 1; c <= book.capitulos; c++) {
        const opt = document.createElement("option");
        opt.value = c;
        opt.textContent = `Capítulo ${c}`;
        if (c === capSelecionado) {
            opt.selected = true;
        }
        selectElement.appendChild(opt);
    }
}

/**
 * Carrega e renderiza o texto do capítulo atual no leitor bíblico.
 */
function carregarCapituloBiblicoAtual() {
    const book = BIBLE_BOOKS.find(b => b.id === bibleState.bookId);
    if (!book) return;

    // Atualiza cabeçalho do capítulo
    const badgeTestamento = document.getElementById("bible-badge-testamento");
    if (badgeTestamento) {
        badgeTestamento.textContent = book.testamento === "AT" ? "ANTIGO TESTAMENTO" : "NOVO TESTAMENTO";
    }

    const chapterHeading = document.getElementById("bible-chapter-heading");
    if (chapterHeading) {
        chapterHeading.textContent = `${book.nome} ${bibleState.chapter}`;
    }

    const badgeVersao = document.getElementById("bible-badge-versao");
    if (badgeVersao) {
        badgeVersao.textContent = "NOVA VERSÃO INTERNACIONAL (NVI)";
    }

    const posLabel = document.getElementById("bible-current-pos-label");
    if (posLabel) {
        posLabel.textContent = `${book.nome} • Capítulo ${bibleState.chapter} de ${book.capitulos}`;
    }

    // Renderiza versículos em formato canônico e contínuo (prosa/parágrafos reais da Bíblia)
    const versesContainer = document.getElementById("bible-verses-list");
    if (versesContainer) {
        const dadosCap = (typeof obterCapituloBiblia === "function")
            ? obterCapituloBiblia(bibleState.bookId, bibleState.chapter)
            : { versiculos: [] };

        const versiculos = dadosCap.versiculos || [];

        if (versiculos.length > 0) {
            const isPoetico = book.grupo === "Poéticos";
            const tamanhoParagrafo = isPoetico ? 2 : 4;
            const marcacoes = carregarMarcacoesBiblia();

            // Agrupa os versículos em parágrafos contínuos
            const paragrafos = [];
            for (let i = 0; i < versiculos.length; i += tamanhoParagrafo) {
                paragrafos.push(versiculos.slice(i, i + tamanhoParagrafo));
            }

            versesContainer.innerHTML = paragrafos.map(pVerses => {
                const innerHtml = pVerses.map(v => {
                    const num = v.numero || v.verso;
                    const verseKey = `${book.id}-${bibleState.chapter}-${num}`;
                    const marcacao = marcacoes[verseKey];
                    const corClasse = marcacao ? ` highlight-${marcacao.cor}` : "";

                    return `<span class="bible-verse-item${corClasse}" data-verse-num="${num}" data-verse-key="${verseKey}" data-verse-text="${escapeHtml(v.texto)}" tabindex="0" role="button" aria-label="Versículo ${num}: clique para marcar"><sup class="bible-verse-num">${num}</sup><span class="verse-text">${escapeHtml(v.texto)}</span></span>`;
                }).join(" ");

                const extraClass = isPoetico ? " bible-poetic-stanza" : "";
                return `<p class="bible-paragraph${extraClass}">${innerHtml}</p>`;
            }).join("");

            // Vincula clique para abrir popover flutuante de marcação
            versesContainer.querySelectorAll(".bible-verse-item").forEach(item => {
                item.addEventListener("click", (e) => {
                    e.stopPropagation();
                    abrirPopoverCores(item);
                });
            });
        } else if (dadosCap.carregando) {
            versesContainer.innerHTML = `
                <div class="bible-loading-state" style="text-align: center; padding: 3rem 1rem; color: #a89885;">
                    <div style="font-family: var(--font-display); font-size: 0.9rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.5rem; color: var(--accent-gold);">Carregando as Sagradas Escrituras</div>
                    <p style="font-family: var(--font-serif); font-style: italic; margin: 0;">Buscando os versículos de ${book.nome} ${bibleState.chapter} na Nova Versão Internacional...</p>
                </div>
            `;
        } else {
            versesContainer.innerHTML = "<p>Texto bíblico sendo preparado para este capítulo.</p>";
        }
    }
}

/**
 * Ajusta o zoom da fonte para leitura.
 */
function ajustarZoomBiblia(delta) {
    bibleState.zoom = Math.min(160, Math.max(80, bibleState.zoom + delta));

    const zoomDisplay = document.getElementById("bible-zoom-level");
    if (zoomDisplay) {
        zoomDisplay.textContent = `${bibleState.zoom}%`;
    }

    const versesContainer = document.getElementById("bible-verses-list");
    if (versesContainer) {
        const basePx = 18;
        const novoPx = (basePx * (bibleState.zoom / 100)).toFixed(1);
        versesContainer.style.fontSize = `${novoPx}px`;
    }
}

/* =====================================================================
   SISTEMA DE MARCAÇÃO DE VERSÍCULOS (HIGHLIGHTS PESSOAIS & PRIVADOS)
   Salvo exclusivamente no localStorage do usuário
   ===================================================================== */
let verseAtivoPopover = null;
let filtroCorAtual = "todas";

function carregarMarcacoesBiblia() {
    try {
        const raw = localStorage.getItem("sola_scriptura_marcacoes_v1");
        return raw ? JSON.parse(raw) : {};
    } catch (e) {
        return {};
    }
}

function salvarMarcacoesBiblia(marcacoes) {
    try {
        localStorage.setItem("sola_scriptura_marcacoes_v1", JSON.stringify(marcacoes));
    } catch (e) {
        console.warn("Erro ao salvar marcações no localStorage:", e);
    }
    atualizarContadorMarcacoes();
}

function definirMarcacaoVersiculo(livroId, capituloNum, versoNum, cor, texto) {
    const marcacoes = carregarMarcacoesBiblia();
    const key = `${livroId}-${capituloNum}-${versoNum}`;
    const book = BIBLE_BOOKS.find(b => b.id === livroId) || { nome: livroId };

    if (!cor || cor === "none") {
        delete marcacoes[key];
        showToast(`Marcação removida de ${book.nome} ${capituloNum}:${versoNum}.`, "info");
    } else {
        marcacoes[key] = {
            id: key,
            livroId: livroId,
            livroNome: book.nome,
            capitulo: parseInt(capituloNum, 10),
            versiculo: parseInt(versoNum, 10),
            referencia: `${book.nome} ${capituloNum}:${versoNum}`,
            texto: texto || "",
            cor: cor,
            data: new Date().toISOString()
        };
        const nomesCores = {
            ouro: "Ouro Imperial",
            verde: "Verde Oliva",
            safira: "Safira Celestial",
            purpura: "Púrpura Real",
            coral: "Coral"
        };
        showToast(`Versículo marcado com ${nomesCores[cor] || cor}!`, "success");
    }

    salvarMarcacoesBiblia(marcacoes);
    atualizarVersiculoNoDOM(key, cor);
    if (document.getElementById("highlights-drawer")?.classList.contains("is-open")) {
        renderizarListaMarcacoes();
    }
}

function atualizarContadorMarcacoes() {
    const marcacoes = carregarMarcacoesBiblia();
    const total = Object.keys(marcacoes).length;

    const countEl = document.getElementById("bible-highlights-count");
    if (countEl) countEl.textContent = total;

    const navCountEl = document.getElementById("nav-highlights-count");
    if (navCountEl) navCountEl.textContent = total;
}

function atualizarVersiculoNoDOM(key, cor) {
    const item = document.querySelector(`.bible-verse-item[data-verse-key="${key}"]`);
    if (!item) return;
    item.classList.remove("highlight-ouro", "highlight-verde", "highlight-safira", "highlight-purpura", "highlight-coral");
    if (cor && cor !== "none") {
        item.classList.add(`highlight-${cor}`);
    }
}

function inicializarPopoverCores() {
    const popover = document.getElementById("verse-highlight-popover");
    if (!popover) return;

    popover.querySelectorAll(".color-dot-btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            if (!verseAtivoPopover) return;
            const cor = btn.getAttribute("data-color");
            definirMarcacaoVersiculo(
                verseAtivoPopover.livroId,
                verseAtivoPopover.capitulo,
                verseAtivoPopover.versoNum,
                cor,
                verseAtivoPopover.texto
            );
            fecharPopoverCores();
        });
    });

    document.addEventListener("click", (e) => {
        if (!popover.contains(e.target) && !e.target.closest(".bible-verse-item")) {
            fecharPopoverCores();
        }
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            fecharPopoverCores();
            fecharGavetaMarcacoes();
        }
    });
}

function abrirPopoverCores(verseEl) {
    const popover = document.getElementById("verse-highlight-popover");
    if (!popover || !verseEl) return;

    const num = verseEl.getAttribute("data-verse-num");
    const key = verseEl.getAttribute("data-verse-key");
    const texto = verseEl.getAttribute("data-verse-text");
    const book = BIBLE_BOOKS.find(b => b.id === bibleState.bookId) || { id: bibleState.bookId, nome: "Bíblia" };

    verseAtivoPopover = {
        element: verseEl,
        livroId: book.id,
        capitulo: bibleState.chapter,
        versoNum: num,
        texto: texto
    };

    popover.style.display = "block";
    const rect = verseEl.getBoundingClientRect();
    const scrollY = window.scrollY || window.pageYOffset;
    const scrollX = window.scrollX || window.pageXOffset;

    const top = rect.top + scrollY - popover.offsetHeight - 10;
    const left = rect.left + scrollX + (rect.width / 2);

    popover.style.top = `${Math.max(10, top)}px`;
    popover.style.left = `${Math.max(160, Math.min(window.innerWidth - 160, left))}px`;
}

function fecharPopoverCores() {
    const popover = document.getElementById("verse-highlight-popover");
    if (popover) {
        popover.style.display = "none";
    }
    verseAtivoPopover = null;
}

function inicializarFiltrosMarcacoes() {
    const pillsContainer = document.getElementById("highlights-filter-pills");
    if (!pillsContainer) return;

    pillsContainer.querySelectorAll(".filter-pill").forEach(pill => {
        pill.addEventListener("click", () => {
            pillsContainer.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("is-active"));
            pill.classList.add("is-active");
            filtroCorAtual = pill.getAttribute("data-filter") || "todas";
            renderizarListaMarcacoes();
        });
    });
}

function abrirGavetaMarcacoes() {
    const drawer = document.getElementById("highlights-drawer");
    const backdrop = document.getElementById("drawer-highlights-backdrop");
    if (!drawer || !backdrop) return;

    fecharPopoverCores();
    renderizarListaMarcacoes();
    drawer.classList.add("is-open");
    drawer.setAttribute("aria-hidden", "false");
    backdrop.classList.add("is-open");
    backdrop.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
}

function fecharGavetaMarcacoes() {
    const drawer = document.getElementById("highlights-drawer");
    const backdrop = document.getElementById("drawer-highlights-backdrop");
    if (!drawer || !backdrop) return;

    drawer.classList.remove("is-open");
    drawer.setAttribute("aria-hidden", "true");
    backdrop.classList.remove("is-open");
    backdrop.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
}

function renderizarListaMarcacoes() {
    const listEl = document.getElementById("highlights-drawer-list");
    if (!listEl) return;

    const marcacoes = carregarMarcacoesBiblia();
    let lista = Object.values(marcacoes);

    if (filtroCorAtual && filtroCorAtual !== "todas") {
        lista = lista.filter(m => m.cor === filtroCorAtual);
    }

    lista.sort((a, b) => new Date(b.data || 0) - new Date(a.data || 0));

    if (lista.length === 0) {
        listEl.innerHTML = `
            <div class="highlights-empty-state">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path>
                </svg>
                <h4>Nenhum Versículo Marcado</h4>
                <p>${filtroCorAtual !== "todas" ? "Nenhum versículo marcado com esta cor." : "Toque em qualquer versículo durante a leitura bíblica para destacá-lo com suas cores favoritas."}</p>
            </div>
        `;
        return;
    }

    listEl.innerHTML = lista.map(item => `
        <div class="highlight-card-item border-${item.cor}" data-verse-key="${item.id}" tabindex="0">
            <div class="highlight-card-header">
                <span class="highlight-card-ref">📖 ${escapeHtml(item.referencia)}</span>
                <button type="button" class="highlight-card-delete-btn" data-key="${item.id}" title="Remover marcação" aria-label="Remover marcação">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                </button>
            </div>
            <p class="highlight-card-text">“${escapeHtml(item.texto)}”</p>
        </div>
    `).join("");

    listEl.querySelectorAll(".highlight-card-item").forEach(card => {
        card.addEventListener("click", (e) => {
            if (e.target.closest(".highlight-card-delete-btn")) return;
            const key = card.getAttribute("data-verse-key");
            const marcacao = marcacoes[key];
            if (!marcacao) return;

            fecharGavetaMarcacoes();
            navegarParaVersiculoMarcado(marcacao);
        });
    });

    listEl.querySelectorAll(".highlight-card-delete-btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const key = btn.getAttribute("data-key");
            const marcacao = marcacoes[key];
            if (marcacao) {
                definirMarcacaoVersiculo(marcacao.livroId, marcacao.capitulo, marcacao.versiculo, "none", "");
                renderizarListaMarcacoes();
            }
        });
    });
}

function navegarParaVersiculoMarcado(marcacao) {
    bibleState.bookId = marcacao.livroId;
    bibleState.chapter = marcacao.capitulo;

    const selectLivro = document.getElementById("bible-select-livro");
    const selectCapitulo = document.getElementById("bible-select-capitulo");

    if (selectLivro) selectLivro.value = marcacao.livroId;
    if (selectCapitulo) {
        preencherSelectCapitulos(selectCapitulo, marcacao.livroId, marcacao.capitulo);
        selectCapitulo.value = marcacao.capitulo;
    }

    carregarCapituloBiblicoAtual();

    setTimeout(() => {
        const verseEl = document.querySelector(`.bible-verse-item[data-verse-key="${marcacao.id}"]`);
        if (verseEl) {
            verseEl.scrollIntoView({ behavior: "smooth", block: "center" });
            verseEl.classList.add("is-target-highlight");
            setTimeout(() => verseEl.classList.remove("is-target-highlight"), 2300);
        }
    }, 350);
}

/**
 * Navega para o próximo ou capítulo anterior.
 */
function navegarCapituloBiblico(delta) {
    const bookIndex = BIBLE_BOOKS.findIndex(b => b.id === bibleState.bookId);
    if (bookIndex === -1) return;

    const bookAtual = BIBLE_BOOKS[bookIndex];
    let novoCap = bibleState.chapter + delta;

    if (novoCap >= 1 && novoCap <= bookAtual.capitulos) {
        bibleState.chapter = novoCap;
    } else if (novoCap < 1 && bookIndex > 0) {
        // Volta para o livro anterior, no último capítulo
        const livroAnterior = BIBLE_BOOKS[bookIndex - 1];
        bibleState.bookId = livroAnterior.id;
        bibleState.chapter = livroAnterior.capitulos;
    } else if (novoCap > bookAtual.capitulos && bookIndex < BIBLE_BOOKS.length - 1) {
        // Avança para o próximo livro, capítulo 1
        const proximoLivro = BIBLE_BOOKS[bookIndex + 1];
        bibleState.bookId = proximoLivro.id;
        bibleState.chapter = 1;
    } else {
        showToast(delta < 0 ? "Você está no início da Bíblia (Gênesis 1)." : "Você chegou ao final da Bíblia (Apocalipse 22).", "info");
        return;
    }

    // Sincroniza selects
    const selectLivro = document.getElementById("bible-select-livro");
    const selectCapitulo = document.getElementById("bible-select-capitulo");

    if (selectLivro) selectLivro.value = bibleState.bookId;
    if (selectCapitulo) {
        preencherSelectCapitulos(selectCapitulo, bibleState.bookId, bibleState.chapter);
    }

    carregarCapituloBiblicoAtual();
    const canvas = document.getElementById("bible-reading-canvas");
    if (canvas) canvas.scrollIntoView({ behavior: "smooth", block: "start" });
}

/**
 * Abre diretamente uma passagem específica no Leitor Bíblico a partir de qualquer link do site.
 */
function abrirPassagemNaBiblia(bookId, capNum) {
    const livroAlvo = BIBLE_BOOKS.find(b => b.id === bookId || b.id.includes(bookId) || bookId.includes(b.id));
    if (livroAlvo) {
        bibleState.bookId = livroAlvo.id;
        bibleState.chapter = Math.min(livroAlvo.capitulos, Math.max(1, capNum || 1));
    } else {
        bibleState.bookId = "salmos";
        bibleState.chapter = capNum || 55;
    }

    const selectLivro = document.getElementById("bible-select-livro");
    const selectCapitulo = document.getElementById("bible-select-capitulo");

    if (selectLivro) selectLivro.value = bibleState.bookId;
    if (selectCapitulo) {
        preencherSelectCapitulos(selectCapitulo, bibleState.bookId, bibleState.chapter);
    }

    trocarAba("biblia");
    carregarCapituloBiblicoAtual();

    const canvas = document.getElementById("bible-reading-canvas");
    if (canvas) canvas.scrollIntoView({ behavior: "smooth", block: "start" });
    showToast(`Lendo ${livroAlvo ? livroAlvo.nome : 'Bíblia'} capítulo ${bibleState.chapter}`, "info");
}


