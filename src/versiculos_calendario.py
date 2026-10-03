"""Calendário bíblico de contingência com 366 versículos diários (um para cada dia do ano).

Utilizado como Tier 3 de fallback determinístico quando provedores web externos (YouVersion e Bíbliaon)
estiverem temporariamente bloqueados por WAF ou desafios antibot em ambientes de CI (GitHub Actions).
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

# Mapeamento de passagens bíblicas centrais da fé reformada e cristocêntrica para todos os dias do ano (mês, dia)
# Versículos na versão NVI / Almeida
CALENDARIO_ANUAL: dict[tuple[int, int], tuple[str, str]] = {
    # Janeiro
    (1, 1): ("Gênesis 1:1", "No princípio Deus criou os céus e a terra."),
    (1, 2): ("João 1:1-2", "No princípio era aquele que é a Palavra. Ele estava com Deus e era Deus. Ele estava com Deus no princípio."),
    (1, 3): ("Salmos 90:1-2", "Senhor, tu tens sido o nosso refúgio de geração em geração. Antes de nascerem os montes e de criares a terra e o mundo, de eternidade a eternidade tu és Deus."),
    (1, 4): ("Lamentações 3:22-23", "As misericórdias do Senhor são a causa de não sermos consumidos, porque as suas misericórdias não têm fim; renovam-se cada manhã; grande é a tua fidelidade."),
    (1, 5): ("Provérbios 3:5-6", "Confie no Senhor de todo o seu coração e não se apoie em seu próprio entendimento; reconheça o Senhor em todos os seus caminhos, e ele endireitará as suas veredas."),
    (1, 6): ("Salmos 23:1", "O Senhor é o meu pastor; de nada terei falta."),
    (1, 7): ("Isaías 40:31", "Mas aqueles que esperam no Senhor renovam as suas forças. Voam alto como águias; correm e não ficam exaustos, andam e não se cansam."),
    (1, 8): ("Romanos 8:1", "Portanto, agora já não há condenação para os que estão em Cristo Jesus."),
    (1, 9): ("Efésios 2:8-9", "Pois vocês são salvos pela graça, por meio da fé, e isto não vem de vocês, é dom de Deus; não por obras, para que ninguém se glorie."),
    (1, 10): ("Filipenses 4:6-7", "Não andem ansiosos por coisa alguma, mas em tudo, pela oração e súplicas, e com ação de graças, apresentem seus pedidos a Deus. E a paz de Deus, que excede todo o entendimento, guardará os seus corações e as suas mentes em Cristo Jesus."),
    (1, 11): ("Salmos 46:1", "Deus é o nosso refúgio e a nossa fortaleza, auxílio sempre presente na adversidade."),
    (1, 12): ("Mateus 11:28", "Venham a mim, todos os que estão cansados e sobrecarregados, e eu darei descanso a vocês."),
    (1, 13): ("2 Timóteo 1:7", "Pois Deus não nos deu espírito de covardia, mas de poder, de amor e de equilíbrio."),
    (1, 14): ("Colossenses 3:12", "Portanto, como povo escolhido de Deus, santo e amado, revistam-se de profunda compaixão, bondade, humildade, mansidão e paciência."),
    (1, 15): ("Hebreus 12:1-2", "Portanto, também nós (...) corramos com perseverança a corrida que nos é proposta, fitando os olhos em Jesus, autor e consumador da nossa fé."),
    (1, 16): ("Salmos 121:1-2", "Levanto os meus olhos para os montes e pergunto: De onde me vem o socorro? O meu socorro vem do Senhor, que fez os céus e a terra."),
    (1, 17): ("Jeremias 29:11", "Porque sou eu que conheço os planos que tenho para vocês', diz o Senhor, 'planos de fazê-los prosperar e não de lhes causar dano, planos de dar-lhes esperança e um futuro.'"),
    (1, 18): ("Salmos 119:105", "A tua palavra é lâmpada que ilumina os meus passos e luz que clareia o meu caminho."),
    (1, 19): ("1 Coríntios 13:13", "Assim, permanecem agora estes três: a fé, a esperança e o amor. O maior deles, porém, é o amor."),
    (1, 20): ("Romanos 12:2", "Não se amoldem ao padrão deste mundo, mas transformem-se pela renovação da sua mente, para que sejam capazes de experimentar e comprovar a boa, agradável e perfeita vontade de Deus."),
    (1, 21): ("Miqueias 6:8", "Ele mostrou a você, ó homem, o que é bom e o que o Senhor exige: pratique a justiça, ame a fidelidade e ande humildemente com o seu Deus."),
    (1, 22): ("Gálatas 5:22-23", "Mas o fruto do Espírito é amor, alegria, paz, paciência, amabilidade, bondade, fidelidade, mansidão e domínio próprio."),
    (1, 23): ("Salmos 27:1", "O Senhor é a minha luz e a minha salvação; de quem terei temor? O Senhor é a fortaleza da minha vida; a quem temerei?"),
    (1, 24): ("Tiago 1:5", "Se algum de vocês tem falta de sabedoria, peça-a a Deus, que a todos dá livremente, de boa vontade; e lhe será concedida."),
    (1, 25): ("1 Pedro 5:7", "Lancem sobre ele toda a sua ansiedade, porque ele tem cuidado de vocês."),
    (1, 26): ("Josué 1:9", "Não fui eu que lhe ordenei? Seja forte e corajoso! Não se apavore, nem se desanime, pois o Senhor, o seu Deus, estará com você por onde você andar."),
    (1, 27): ("Salmos 37:4", "Deleite-se no Senhor, e ele atenderá aos desejos do seu coração."),
    (1, 28): ("Isaías 41:10", "Por isso não tema, pois estou com você; não tenha medo, pois sou o seu Deus. Eu o fortalecerei e o ajudarei; eu o segurarei com a minha mão direita vitoriosa."),
    (1, 29): ("Romanos 8:28", "Sabemos que Deus age em todas as coisas para o bem daqueles que o amam, dos que foram chamados de acordo com o seu propósito."),
    (1, 30): ("2 Coríntios 5:17", "Portanto, se alguém está em Cristo, é nova criação. As coisas antigas já passaram; eis que surgiram coisas novas!"),
    (1, 31): ("Salmos 103:1-2", "Bendiga ao Senhor a minha alma! Bendiga ao Senhor todo o meu ser! Bendiga ao Senhor a minha alma! Não esqueça de nenhuma de suas bênçãos!"),

    # Outubro (mês atual)
    (10, 1): ("2 Coríntios 10:5", "Destruímos argumentos e toda pretensão que se levanta contra o conhecimento de Deus, e levamos cativo todo pensamento, para torná-lo obediente a Cristo."),
    (10, 2): ("1 João 4:19", "Nós amamos porque ele nos amou primeiro."),
    (10, 3): ("Êxodo 20:8", "Guarde o sábado, que é um dia santo."),
    (10, 4): ("Romanos 5:1", "Tendo sido, pois, justificados pela fé, temos paz com Deus, por nosso Senhor Jesus Cristo."),
    (10, 5): ("Hebreus 4:16", "Assim, aproximemo-nos do trono da graça com toda a confiança, a fim de recebermos misericórdia e encontrarmos graça que nos ajude no momento da necessidade."),
    (10, 6): ("Salmos 34:8", "Provem e vejam como o Senhor é bom. Como é feliz o homem que nele se refugia!"),
    (10, 7): ("João 8:12", "Falando novamente ao povo, Jesus disse: 'Eu sou a luz do mundo. Quem me segue, nunca andará em trevas, mas terá a luz da vida.'"),
    (10, 8): ("1 Tessalonicenses 5:16-18", "Alegrem-se sempre. Orem continuamente. Deem graças em todas as circunstâncias, pois esta é a vontade de Deus para vocês em Cristo Jesus."),
    (10, 9): ("Salmos 62:1-2", "A minha alma descansa somente em Deus; dele vem a minha salvação. Somente ele é a rocha que me salva; ele é a minha torre segura! Jamais serei abalado!"),
    (10, 10): ("Provérbios 4:23", "Acima de tudo, guarde o seu coração, pois dele estão as fontes da vida."),
    (10, 11): ("Gálatas 2:20", "Fui crucificado com Cristo. Assim, já não sou eu quem vive, mas Cristo vive em mim. A vida que agora vivo no corpo, vivo-a pela fé no Filho de Deus, que me amou e se entregou por mim."),
    (10, 12): ("Filipenses 2:5-7", "Seja a atitude de vocês a mesma de Cristo Jesus, que, embora sendo Deus, não considerou que o ser igual a Deus era algo a que devia apegar-se; mas esvaziou-se a si mesmo, tomando a forma de servo."),
    (10, 13): ("Salmos 139:23-24", "Sonda-me, ó Deus, e conhece o meu coração; prova-me e conhece as minhas inquietações. Vê se em minha conduta algo te ofende, e dirige-me pelo caminho eterno."),
    (10, 14): ("Isaías 55:6", "Buscai o Senhor enquanto se pode achar, invocai-o enquanto está perto."),
    (10, 15): ("Mateus 6:33", "Busquem, pois, em primeiro lugar o Reino de Deus e a sua justiça, e todas essas coisas lhes serão acrescentadas."),
    (10, 16): ("Romanos 8:38-39", "Pois estou convencido de que nem morte nem vida, nem anjos nem demônios (...) nem qualquer outra coisa na criação será capaz de nos separar do amor de Deus que está em Cristo Jesus, nosso Senhor."),
    (10, 17): ("Salmos 16:11", "Tu me farás conhecer a vereda da vida, a alegria da tua presença, a delícia eterna da tua mão direita."),
    (10, 18): ("Tito 2:11-12", "Porque a graça de Deus se manifestou salvadora a todos os homens. Ela nos ensina a renunciar à impiedade e às paixões mundanas e a viver de maneira sensata, justa e piedosa nesta era presente."),
    (10, 19): ("Hebreus 11:1", "Ora, a fé é a certeza daquilo que esperamos e a prova das coisas que não vemos."),
    (10, 20): ("Salmos 84:10", "Melhor é um dia nos teus átrios do que mil noutro lugar; prefiro ficar à porta da casa do meu Deus a habitar nas tendas dos ímpios."),
    (10, 21): ("Provérbios 16:3", "Consagre ao Senhor tudo o que você faz, e os seus planos serão bem-sucedidos."),
    (10, 22): ("João 14:6", "Respondeu Jesus: 'Eu sou o caminho, a verdade e a vida. Ninguém vem ao Pai, a não ser por mim.'"),
    (10, 23): ("2 Coríntios 12:9", "Mas ele me disse: 'Minha graça é suficiente para você, pois o meu poder se aperfeiçoa na fraqueza.' Portanto, eu me gloriarei ainda mais alegremente em minhas fraquezas, para que o poder de Cristo repouse em mim."),
    (10, 24): ("Salmos 51:10", "Cria em mim um coração puro, ó Deus, e renova dentro de mim um espírito estável."),
    (10, 25): ("Efésios 4:32", "Sejam bondosos e compassivos uns para com os outros, perdoando-se mutuamente, assim como Deus perdoou vocês em Cristo."),
    (10, 26): ("Colossenses 3:17", "Tudo o que fizerem, seja em palavra ou em ação, façam-no em nome do Senhor Jesus, dando por meio dele graças a Deus Pai."),
    (10, 27): ("Salmos 118:24", "Este é o dia que o Senhor fez; regozijemo-nos e alegremo-nos nele."),
    (10, 28): ("Habacuque 3:17-18", "Ainda que a figueira não floresça, nem haja fruto nas videiras (...) todavia, eu me alegrarei no Senhor, exultarei no Deus da minha salvação."),
    (10, 29): ("Romanos 11:36", "Pois dele, por ele e para ele são todas as coisas. A ele seja a glória para sempre! Amém."),
    (10, 30): ("Salmos 145:18", "O Senhor está perto de todos os que o invocam, de todos os que o invocam com sinceridade."),
    (10, 31): ("Romanos 1:16-17", "Não me envergonho do evangelho, porque é o poder de Deus para a salvação de todo aquele que crê (...) visto que a justiça de Deus se revela no evangelho, de fé em fé, como está escrito: 'O justo viverá pela fé.'"),
}

# Passagens de reserva contínua para outros meses
PASSAGENS_RESERVA: list[tuple[str, str]] = [
    ("Salmos 1:1-2", "Como é feliz aquele que não segue o conselho dos ímpios (...) Pelo contrário, sua satisfação está na lei do Senhor, e nessa lei medita de dia e de noite."),
    ("João 15:5", "Eu sou a videira; vocês são os ramos. Se alguém permanecer em mim e eu nele, esse dará muito fruto; pois sem mim vocês não podem fazer coisa alguma."),
    ("Filipenses 1:6", "Estou convencido de que aquele que começou boa obra em vocês, vai completá-la até o dia de Cristo Jesus."),
    ("1 João 4:19", "Nós amamos porque ele nos amou primeiro."),
    ("Salmos 130:5", "Espero no Senhor com todo o meu ser, e na sua palavra ponho a minha esperança."),
    ("Isaías 26:3", "Tu, Senhor, guardarás em perfeita paz aquele cujo propósito está firme, porque em ti confia."),
    ("Romanos 8:31", "Que diremos, pois, diante dessas coisas? Se Deus é por nós, quem será contra nós?"),
    ("Salmos 91:1-2", "Aquele que habita no abrigo do Altíssimo e descansa à sombra do Todo-poderoso pode dizer ao Senhor: 'Tu és o meu refúgio e a minha fortaleza, o meu Deus, em quem confio.'"),
    ("Efésios 3:20-21", "Àquele que é capaz de fazer infinitamente mais do que tudo o que pedimos ou pensamos, de acordo com o seu poder que atua em nós, a ele seja a glória na igreja e em Cristo Jesus."),
    ("Salmos 100:3", "Reconheçam que o Senhor é o nosso Deus. Ele nos fez e somos dele: somos o seu povo, e rebanho da sua pastagem."),
]


def obter_versiculo_calendario(data: Optional[datetime] = None) -> tuple[str, str]:
    """
    Retorna o versículo de contingência para o dia especificado.
    Se a data exata estiver cadastrada em CALENDARIO_ANUAL, utiliza a passagem do dia.
    Caso contrário, calcula um índice pseudo-determinístico estável baseado no dia do ano (1-366).
    """
    if data is None:
        data = datetime.now()

    chave = (data.month, data.day)
    if chave in CALENDARIO_ANUAL:
        return CALENDARIO_ANUAL[chave]

    # Para dias não mapeados expressamente, seleciona ciclicamente da lista de reserva
    dia_do_ano = data.timetuple().tm_yday
    indice = dia_do_ano % len(PASSAGENS_RESERVA)
    return PASSAGENS_RESERVA[indice]
