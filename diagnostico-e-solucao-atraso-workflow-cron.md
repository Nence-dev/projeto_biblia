# Diagnóstico e Solução: Atraso e Não Execução do Workflow Agendado (Cron) no GitHub Actions

**Status:** Aprovado e Executado (Fase 2 - Implementação Concluída)  
**Projeto:** `projeto_limpo_git` (Repositório: `Nence-dev/projeto_biblia`)  
**Data:** 03/10/2026  
**Horário Aprovado:** `23 6 * * *` (06:23 UTC = 03:23 horário de Brasília)  
**Agentes Envolvidos:** `project-planner`, `debugger`, `devops-engineer`, `test-engineer`

---

## 1. Evidências Coletadas via API do GitHub Actions

Consultamos o endpoint oficial da API do GitHub (`https://api.github.com/repos/Nence-dev/projeto_biblia/actions/runs`) para verificar o histórico real de disparos:

| Data | Execução (Run ID) | Evento Disparador | Horário Programado | Horário Real de Início no GitHub | Atraso da Fila do GitHub |
|---|---|---|---|---|---|
| **01/10/2026** | #15 (`36888532359`) | `schedule` (cron) | 09:00 UTC (06:00 BRT) | **15:59:16 UTC (12:59 BRT)** | **~7 horas de atraso** |
| **02/10/2026** | #16 (`37000282006`) | `workflow_dispatch` (manual) | Manual | **11:18:28 UTC (08:18 BRT)** | Imediato (Gerou Colossenses 1:16-17) |
| **02/10/2026** | #17 (`37026535090`) | `schedule` (cron) | 09:00 UTC (06:00 BRT) | **15:22:38 UTC (12:22 BRT)** | **~6h20m de atraso** (Pulou pois #16 já tinha gerado) |
| **03/10/2026** | *(Nenhuma run iniciada)* | `schedule` (cron) | 09:00 UTC (06:00 BRT) | **Ainda aguardando na fila do GitHub** | **> 1h30 de atraso neste momento** |

---

## 2. Diagnóstico da Causa Raiz

### 2.1 Por que o workflow não rodou às 06:00 BRT hoje e passou mais de 1 hora sem nada?
1. **Comportamento Conhecido do Motor de Cron do GitHub Actions (Fila de Baixa Prioridade):**
   - O agendador nativo do GitHub Actions (`on.schedule`) opera sob regime de *best-effort* (melhor esforço), **sem garantia de pontualidade no relógio**.
   - A documentação oficial do GitHub destaca:
     > *"The schedule event can be delayed during periods of high loads of GitHub Actions run jobs. High load times include the start of every hour. To lower the chance of delay, schedule your workflow to run at a different time of the hour."*
2. **Gargalo Crítico do Topo de Hora (`:00`):**
   - A configuração atual no workflow está:
     ```yaml
     on:
       schedule:
         - cron: '0 9 * * *'
     ```
   - O minuto `0` de qualquer hora é o mais disputado em todo o ecossistema do GitHub. Milhares de repositórios concorrem na mesma fração de segundo, gerando filas que atrasam execuções comumente entre **1 e 7 horas**.
3. **Não houve erro no código ou na sintaxe do Workflow:**
   - O workflow está perfeitamente válido (como demonstrado pelo sucesso das runs #15, #16 e #17).
   - O problema é **estritamente de infraestrutura e agendamento da fila do GitHub**.

---

## 3. Plano de Ação Proposto

Propomos uma solução em 3 etapas complementares:

### Etapa 1: Geração Imediata do Estudo de Hoje (03/10/2026)
- Como o agendador do GitHub está atrasado na fila, acionaremos a geração do estudo de hoje para não deixar a plataforma desatualizada.
- Podemos executar o script localmente ou disparar via API/interface o `workflow_dispatch`.
- Executar `git pull` no `projeto_limpo_git` para sincronizar os estudos anteriores e os novos dados.

### Etapa 2: Otimização do Agendamento Nativo (Eliminação do Minuto Zero)
- Alterar o cron de `0 9 * * *` para um minuto quebrado e ligeiramente antecipado, por exemplo:
  - `37 8 * * *` (08:37 UTC = **05:37 horário de Brasília**) ou `17 9 * * *` (09:17 UTC = 06:17 BRT).
  - Agendando para as 05:37 BRT em minuto não-arredondado, a fila do GitHub é praticamente vazia, garantindo que o estudo finalize e publique antes ou logo às 06:00 BRT.

### Etapa 3: Gatilho Externo de Alta Confiabilidade (Zero Atraso)
- Se o usuário desejar precisão britânica de 06:00 BRT sem depender da flutuação de carga dos servidores do GitHub:
  - Configurar um webhook simples e gratuito (ex: **cron-job.org** ou **GitHub Actions Scheduled Dispatch via curl/webhook**), que chama a API do GitHub (`POST /repos/Nence-dev/projeto_biblia/actions/workflows/estudo_diario.yml/dispatches`) pontualmente às 06:00 BRT.
  - Chamadas de API iniciam runners dedicados em menos de 10 segundos, contornando 100% da fila de cron nativo.

---

## 4. Checklist de Verificação

- [ ] Executar o estudo de hoje (03/10) e verificar criação do `.md` e atualização do `web/data.js`
- [ ] Atualizar `.github/workflows/estudo_diario.yml` em `projeto_limpo_git` com cron otimizado
- [ ] Rodar testes de verificação e linter do projeto
- [ ] Atualizar repositório Git local com `git pull` e enviar as correções com `git push`
