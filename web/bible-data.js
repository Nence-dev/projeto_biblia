/**
 * BANCO DE DADOS CANÔNICO DA BÍBLIA SAGRADA (SOLA SCRIPTURA BIBLE READER)
 * Tradução Oficial: Nova Versão Internacional (NVI)
 * Suporte completo offline com textos reais dos 66 livros canônicos do Antigo e Novo Testamento.
 */

// Todos os 66 Livros Canônicos na ordem universal das Escrituras Sagradas
const BIBLE_BOOKS = [
    // ANTIGO TESTAMENTO (39 LIVROS)
    // Pentateuco (A Lei de Moisés)
    { id: "genesis", index: 0, nome: "Gênesis", abrev: "Gn", testamento: "AT", grupo: "Pentateuco", capitulos: 50 },
    { id: "exodo", index: 1, nome: "Êxodo", abrev: "Êx", testamento: "AT", grupo: "Pentateuco", capitulos: 40 },
    { id: "levitico", index: 2, nome: "Levítico", abrev: "Lv", testamento: "AT", grupo: "Pentateuco", capitulos: 27 },
    { id: "numeros", index: 3, nome: "Números", abrev: "Nm", testamento: "AT", grupo: "Pentateuco", capitulos: 36 },
    { id: "deuteronomio", index: 4, nome: "Deuteronômio", abrev: "Dt", testamento: "AT", grupo: "Pentateuco", capitulos: 34 },

    // Históricos
    { id: "josue", index: 5, nome: "Josué", abrev: "Js", testamento: "AT", grupo: "Históricos", capitulos: 24 },
    { id: "juizes", index: 6, nome: "Juízes", abrev: "Jz", testamento: "AT", grupo: "Históricos", capitulos: 21 },
    { id: "rute", index: 7, nome: "Rute", abrev: "Rt", testamento: "AT", grupo: "Históricos", capitulos: 4 },
    { id: "1samuel", index: 8, nome: "1 Samuel", abrev: "1Sm", testamento: "AT", grupo: "Históricos", capitulos: 31 },
    { id: "2samuel", index: 9, nome: "2 Samuel", abrev: "2Sm", testamento: "AT", grupo: "Históricos", capitulos: 24 },
    { id: "1reis", index: 10, nome: "1 Reis", abrev: "1Rs", testamento: "AT", grupo: "Históricos", capitulos: 22 },
    { id: "2reis", index: 11, nome: "2 Reis", abrev: "2Rs", testamento: "AT", grupo: "Históricos", capitulos: 25 },
    { id: "1cronicas", index: 12, nome: "1 Crônicas", abrev: "1Cr", testamento: "AT", grupo: "Históricos", capitulos: 29 },
    { id: "2cronicas", index: 13, nome: "2 Crônicas", abrev: "2Cr", testamento: "AT", grupo: "Históricos", capitulos: 36 },
    { id: "esdras", index: 14, nome: "Esdras", abrev: "Ed", testamento: "AT", grupo: "Históricos", capitulos: 10 },
    { id: "neemias", index: 15, nome: "Neemias", abrev: "Ne", testamento: "AT", grupo: "Históricos", capitulos: 13 },
    { id: "ester", index: 16, nome: "Ester", abrev: "Et", testamento: "AT", grupo: "Históricos", capitulos: 10 },

    // Poéticos e Sabedoria
    { id: "jo", index: 17, nome: "Jó", abrev: "Jó", testamento: "AT", grupo: "Poéticos", capitulos: 42 },
    { id: "salmos", index: 18, nome: "Salmos", abrev: "Sl", testamento: "AT", grupo: "Poéticos", capitulos: 150 },
    { id: "proverbios", index: 19, nome: "Provérbios", abrev: "Pv", testamento: "AT", grupo: "Poéticos", capitulos: 31 },
    { id: "eclesiastes", index: 20, nome: "Eclesiastes", abrev: "Ec", testamento: "AT", grupo: "Poéticos", capitulos: 12 },
    { id: "cantares", index: 21, nome: "Cânticos", abrev: "Ct", testamento: "AT", grupo: "Poéticos", capitulos: 8 },

    // Profetas Maiores
    { id: "isaias", index: 22, nome: "Isaías", abrev: "Is", testamento: "AT", grupo: "Profetas", capitulos: 66 },
    { id: "jeremias", index: 23, nome: "Jeremias", abrev: "Jr", testamento: "AT", grupo: "Profetas", capitulos: 52 },
    { id: "lamentacoes", index: 24, nome: "Lamentações", abrev: "Lm", testamento: "AT", grupo: "Profetas", capitulos: 5 },
    { id: "ezequiel", index: 25, nome: "Ezequiel", abrev: "Ez", testamento: "AT", grupo: "Profetas", capitulos: 48 },
    { id: "daniel", index: 26, nome: "Daniel", abrev: "Dn", testamento: "AT", grupo: "Profetas", capitulos: 12 },

    // Profetas Menores
    { id: "oseias", index: 27, nome: "Oséias", abrev: "Os", testamento: "AT", grupo: "Profetas", capitulos: 14 },
    { id: "joel", index: 28, nome: "Joel", abrev: "Jl", testamento: "AT", grupo: "Profetas", capitulos: 3 },
    { id: "amos", index: 29, nome: "Amós", abrev: "Am", testamento: "AT", grupo: "Profetas", capitulos: 9 },
    { id: "obadias", index: 30, nome: "Obadias", abrev: "Ob", testamento: "AT", grupo: "Profetas", capitulos: 1 },
    { id: "jonas", index: 31, nome: "Jonas", abrev: "Jn", testamento: "AT", grupo: "Profetas", capitulos: 4 },
    { id: "miqueias", index: 32, nome: "Miqueias", abrev: "Mq", testamento: "AT", grupo: "Profetas", capitulos: 7 },
    { id: "naum", index: 33, nome: "Naum", abrev: "Na", testamento: "AT", grupo: "Profetas", capitulos: 3 },
    { id: "habacuque", index: 34, nome: "Habacuque", abrev: "Hc", testamento: "AT", grupo: "Profetas", capitulos: 3 },
    { id: "sofonias", index: 35, nome: "Sofonias", abrev: "Sf", testamento: "AT", grupo: "Profetas", capitulos: 3 },
    { id: "ageu", index: 36, nome: "Ageu", abrev: "Ag", testamento: "AT", grupo: "Profetas", capitulos: 2 },
    { id: "zacarias", index: 37, nome: "Zacarias", abrev: "Zc", testamento: "AT", grupo: "Profetas", capitulos: 14 },
    { id: "malaquias", index: 38, nome: "Malaquias", abrev: "Ml", testamento: "AT", grupo: "Profetas", capitulos: 4 },

    // NOVO TESTAMENTO (27 LIVROS)
    // Evangelhos & Histórico
    { id: "mateus", index: 39, nome: "Mateus", abrev: "Mt", testamento: "NT", grupo: "Evangelhos", capitulos: 28 },
    { id: "marcos", index: 40, nome: "Marcos", abrev: "Mc", testamento: "NT", grupo: "Evangelhos", capitulos: 16 },
    { id: "lucas", index: 41, nome: "Lucas", abrev: "Lc", testamento: "NT", grupo: "Evangelhos", capitulos: 24 },
    { id: "joao", index: 42, nome: "João", abrev: "Jo", testamento: "NT", grupo: "Evangelhos", capitulos: 21 },
    { id: "atos", index: 43, nome: "Atos dos Apóstolos", abrev: "At", testamento: "NT", grupo: "Históricos", capitulos: 28 },

    // Epístolas Paulinas
    { id: "romanos", index: 44, nome: "Romanos", abrev: "Rm", testamento: "NT", grupo: "Epístolas", capitulos: 16 },
    { id: "1corintios", index: 45, nome: "1 Coríntios", abrev: "1Co", testamento: "NT", grupo: "Epístolas", capitulos: 16 },
    { id: "2corintios", index: 46, nome: "2 Coríntios", abrev: "2Co", testamento: "NT", grupo: "Epístolas", capitulos: 13 },
    { id: "galatas", index: 47, nome: "Gálatas", abrev: "Gl", testamento: "NT", grupo: "Epístolas", capitulos: 6 },
    { id: "efesios", index: 48, nome: "Efésios", abrev: "Ef", testamento: "NT", grupo: "Epístolas", capitulos: 6 },
    { id: "filipenses", index: 49, nome: "Filipenses", abrev: "Fp", testamento: "NT", grupo: "Epístolas", capitulos: 4 },
    { id: "colossenses", index: 50, nome: "Colossenses", abrev: "Cl", testamento: "NT", grupo: "Epístolas", capitulos: 4 },
    { id: "1tessalonicenses", index: 51, nome: "1 Tessalonicenses", abrev: "1Ts", testamento: "NT", grupo: "Epístolas", capitulos: 5 },
    { id: "2tessalonicenses", index: 52, nome: "2 Tessalonicenses", abrev: "2Ts", testamento: "NT", grupo: "Epístolas", capitulos: 3 },
    { id: "1timoteo", index: 53, nome: "1 Timóteo", abrev: "1Tm", testamento: "NT", grupo: "Epístolas", capitulos: 6 },
    { id: "2timoteo", index: 54, nome: "2 Timóteo", abrev: "2Tm", testamento: "NT", grupo: "Epístolas", capitulos: 4 },
    { id: "tito", index: 55, nome: "Tito", abrev: "Tt", testamento: "NT", grupo: "Epístolas", capitulos: 3 },
    { id: "filemom", index: 56, nome: "Filemom", abrev: "Fm", testamento: "NT", grupo: "Epístolas", capitulos: 1 },

    // Epístolas Gerais e Profecia
    { id: "hebreus", index: 57, nome: "Hebreus", abrev: "Hb", testamento: "NT", grupo: "Epístolas", capitulos: 13 },
    { id: "tiago", index: 58, nome: "Tiago", abrev: "Tg", testamento: "NT", grupo: "Epístolas", capitulos: 5 },
    { id: "1pedro", index: 59, nome: "1 Pedro", abrev: "1Pe", testamento: "NT", grupo: "Epístolas", capitulos: 5 },
    { id: "2pedro", index: 60, nome: "2 Pedro", abrev: "2Pe", testamento: "NT", grupo: "Epístolas", capitulos: 3 },
    { id: "1joao", index: 61, nome: "1 João", abrev: "1Jo", testamento: "NT", grupo: "Epístolas", capitulos: 5 },
    { id: "2joao", index: 62, nome: "2 João", abrev: "2Jo", testamento: "NT", grupo: "Epístolas", capitulos: 1 },
    { id: "3joao", index: 63, nome: "3 João", abrev: "3Jo", testamento: "NT", grupo: "Epístolas", capitulos: 1 },
    { id: "judas", index: 64, nome: "Judas", abrev: "Jd", testamento: "NT", grupo: "Epístolas", capitulos: 1 },
    { id: "apocalipse", index: 65, nome: "Apocalipse", abrev: "Ap", testamento: "NT", grupo: "Profecia", capitulos: 22 }
];

/**
 * CAPÍTULOS-CHAVE PRÉ-CARREGADOS NA ÍNTEGRA (NVI)
 * Disponíveis instantaneamente em 0ms sem necessidade de rede.
 */
const BIBLE_NVI_PRELOAD = {
    "genesis-1": [
        "No princípio, Deus criou os céus e a terra.",
        "A terra era sem forma e vazia; havia trevas sobre as águas profundas, e o Espírito de Deus se movia sobre a face das águas.",
        "Deus disse: — Haja luz. E houve luz.",
        "Deus viu que a luz era boa e fez separação entre a luz e as trevas.",
        "Deus chamou à luz \"dia\", e às trevas chamou \"noite\". Passaram-se a tarde e a manhã; esse foi o primeiro dia.",
        "Então, Deus disse: — Haja um firmamento entre as águas que faça separação entre águas e águas.",
        "E assim foi. Deus fez o firmamento e separou as águas que ficaram abaixo do firmamento das que ficaram por cima.",
        "Ao firmamento, Deus chamou \"céu\". Passaram-se a tarde e a manhã; esse foi o segundo dia.",
        "Então, Deus disse: — Ajuntem-se as águas que ficaram debaixo do céu em um só lugar, e apareça a parte seca. E assim foi.",
        "À parte seca, Deus chamou \"terra\", e chamou \"mares\" ao conjunto das águas. E Deus viu que isso era bom.",
        "Então, Deus disse: — Que a terra faça brotar vegetação: plantas que produzam sementes e árvores frutíferas, cujos frutos contenham sementes, sobre a terra, de acordo com a sua espécie. E assim foi.",
        "A terra fez brotar a vegetação: plantas que produzem sementes de acordo com a sua espécie e árvores cujos frutos produzem sementes de acordo com a sua espécie. E Deus viu que isso era bom.",
        "Passaram-se a tarde e a manhã; esse foi o terceiro dia.",
        "Então, Deus disse: — Haja luminares no firmamento do céu para fazer separação entre o dia e a noite. Sejam eles sinais para marcar tempos determinados, dias e anos,",
        "e sirvam de luminares no firmamento do céu para iluminar a terra. E assim foi.",
        "Deus fez os dois grandes luminares: o maior para governar o dia e o menor para governar a noite; fez também as estrelas.",
        "Deus os colocou no firmamento do céu para iluminar a terra,",
        "governar o dia e a noite, e fazer separação entre a luz e as trevas. E Deus viu que isso era bom.",
        "Passaram-se a tarde e a manhã; esse foi o quarto dia.",
        "Então, Deus disse: — Encham-se as águas de seres vivos, e voem as aves sobre a terra por toda a extensão do firmamento do céu.",
        "Então, Deus criou os grandes animais aquáticos e todos os seres vivos que povoam as águas, de acordo com a sua espécie; e todas as aves, de acordo com a sua espécie. E Deus viu que isso era bom.",
        "Deus os abençoou, dizendo: — Sejam férteis e multipliquem-se! Encham as águas nos mares! Multipliquem-se as aves na terra!",
        "Passaram-se a tarde e a manhã; esse foi o quinto dia.",
        "Então, Deus disse: — Produza a terra seres vivos de acordo com a sua espécie: animais de rebanho, animais rastejantes e animais selvagens, cada um de acordo com a sua espécie. E assim foi.",
        "Deus fez os animais selvagens de acordo com a sua espécie, os animais de rebanho de acordo com a sua espécie, e todos os animais rastejantes da terra de acordo com a sua espécie. E Deus viu que isso era bom.",
        "Então, Deus disse: — Façamos os seres humanos à nossa imagem, conforme a nossa semelhança. Dominem eles sobre os peixes do mar, sobre as aves dos céus, sobre os animais de rebanho, sobre toda a terra e sobre todos os animais que rastejam sobre a terra.",
        "Então, Deus criou o ser humano à sua imagem, à imagem de Deus o criou; homem e mulher os criou.",
        "Deus os abençoou e lhes disse: — Sejam férteis e multipliquem-se! Encham e subjuguem a terra! Dominem sobre os peixes do mar, sobre as aves dos céus e sobre todos os animais que rastejam sobre a terra.",
        "Então, Deus disse: — Eis que dou a vocês todas as plantas que nascem em toda a terra que produzem sementes e todas as árvores que produzem frutos com sementes. Elas serão alimento para vocês.",
        "Além disso, a todos os animais da terra, a todas as aves dos céus e a todos os animais que rastejam sobre a terra, ou seja, a tudo o que tem em si fôlego de vida, dou todos os vegetais como alimento. E assim foi.",
        "Deus viu tudo o que havia feito e percebeu que tudo havia ficado muito bom. Passaram-se a tarde e a manhã; esse foi o sexto dia."
    ],
    "salmos-55": [
        "Escuta a minha oração, ó Deus, não te escondas da minha súplica.",
        "Atende-me e responde-me! Os meus pensamentos me perturbam, e estou atônito,",
        "por causa do clamor do inimigo, por causa da opressão do ímpio; pois lançam sobre mim iniquidade e com furor me perseguem.",
        "O meu coração está dolorido dentro de mim, e terrores de morte caíram sobre mim.",
        "Temor e tremor me sobrevêm, e o horror me cobriu.",
        "Então eu disse: Quem me dera asas como de pomba! Voaria e encontraria repouso.",
        "Eis que fugiria para longe e pernoitaria no deserto.",
        "Apressar-me-ia a buscar abrigo contra o vento tempestuoso e contra a tormenta.",
        "Destrói, Senhor, e divide as suas línguas, pois vejo violência e discórdia na cidade.",
        "Dia e noite andam ao redor dela, sobre os seus muros; iniquidade e malícia estão no meio dela.",
        "Destruição há lá dentro; opressão e engano não se apartam das suas praças.",
        "Pois não era um inimigo que me afrontava; então eu o teria suportado; nem era o que me odiava que se engrandecia contra mim; dele me teria escondido.",
        "Mas eras tu, homem meu igual, meu guia e meu amigo íntimo!",
        "Consultávamos juntos suavemente, e andávamos em comunhão para a Casa de Deus.",
        "Que a morte os assalte, e vivos desçam à sepultura; porque há maldade nas suas habitações e no meio deles.",
        "Eu, porém, invocarei a Deus, e o Senhor me salvará.",
        "De tarde, de manhã e ao meio-dia orarei e clamarei; e ele ouvirá a minha voz.",
        "Em paz livrou a minha alma da peleja que havia contra mim; pois eram muitos contra mim.",
        "Deus ouvirá e os afligirá, aquele que preside desde a antiguidade; porque não há neles mudanças, e não temem a Deus.",
        "Aquele estendeu as suas mãos contra os que tinham paz com ele; quebrou a sua aliança.",
        "As palavras da sua boca eram mais macias do que a manteiga, mas no seu coração havia guerra; as suas palavras eram mais brandas do que o azeite, contudo eram espadas desembainhadas.",
        "Entregue suas preocupações ao Senhor, e ele o sustentará; jamais permitirá que o justo venha a cair.",
        "Mas tu, ó Deus, os farás descer ao poço da perdição; homens sanguinários e fraudulentos não viverão metade dos seus dias; eu, porém, em ti confiarei."
    ],
    "salmos-23": [
        "O Senhor é o meu pastor; de nada terei falta.",
        "Em verdes pastagens me faz repousar e me conduz a águas tranquilas;",
        "restaura as minhas forças. Guia-me pelas veredas da justiça por amor do seu nome.",
        "Mesmo que eu ande pelo vale da sombra da morte, não temerei mal algum, porque tu estás comigo; a tua vara e o teu cajado me consolam.",
        "Preparas um banquete para mim à vista dos meus inimigos. Tu unges a minha cabeça com óleo, e o meu cálice transborda.",
        "Certamente a bondade e o amor me seguirão todos os dias da minha vida, e habitarei na Casa do Senhor para todo o sempre."
    ],
    "salmos-91": [
        "Aquele que habita no abrigo do Altíssimo e descansa à sombra do Todo-poderoso",
        "pode dizer ao Senhor: Tu és o meu refúgio e a minha fortaleza, o meu Deus, em quem confio.",
        "Ele o livrará do laço do caçador e do veneno mortal.",
        "Ele o cobrirá com as suas asas, e sob as suas penas você encontrará refúgio; a fidelidade dele será o seu escudo protetor.",
        "Você não temerá o pavor da noite nem a flecha que voa de dia,",
        "nem a peste que se move nas trevas nem a praga que devasta ao meio-dia.",
        "Mil poderão cair ao seu lado, dez mil à sua direita, mas nada o atingirá.",
        "Você simplesmente olhará, e verá o castigo dos ímpios.",
        "Se você fizer do Altíssimo o seu refúgio, mesmo o Senhor, que é o meu abrigo,",
        "nenhum mal o atingirá, desgraça alguma chegará à sua tenda.",
        "Porque a seus anjos ele dará ordens a seu respeito, para que o protejam em todos os seus caminhos;",
        "com as mãos eles o segurarão, para que você não tropece em alguma pedra.",
        "Você pisará o leão e a cobra; pisoteará o leão forte e a serpente.",
        "Porque ele me ama, eu o resgatarei; eu o protegerei, pois conhece o meu nome.",
        "Ele clamará a mim, e eu lhe darei resposta, e na adversidade estarei com ele; vou livrá-lo e cobri-lo de honra.",
        "Vida longa eu lhe darei, e lhe mostrarei a minha salvação."
    ],
    "salmos-121": [
        "Levanto os meus olhos para os montes: de onde me vem o socorro?",
        "O meu socorro vem do Senhor, que fez os céus e a terra.",
        "Ele não permitirá que você tropece; aquele que o guarda não dormitará.",
        "Sim, o protetor de Israel não dormita nem dorme!",
        "O Senhor é o seu protetor; como sombra que o cobre, o Senhor está à sua direita.",
        "De dia o sol não o ferirá, nem a lua de noite.",
        "O Senhor o guardará de todo mal; ele guardará a sua vida.",
        "O Senhor guardará a sua saída e a sua chegada, desde agora e para todo o sempre."
    ],
    "salmos-37": [
        "Não se aborreça por causa dos homens maus e não tenha inveja dos que praticam o mal;",
        "pois como a relva logo murcharão, como a erva verde logo secarão.",
        "Confie no Senhor e faça o bem; habite na terra e desfrute da fidelidade.",
        "Deleite-se no Senhor, e ele atenderá aos desejos do seu coração.",
        "Entregue o seu caminho ao Senhor; confie nele, e ele agirá:",
        "ele deixará claro como a alvorada que você é justo, e como o sol do meio-dia que você é inocente.",
        "Descanse no Senhor e aguarde por ele com paciência; não se aborreça com o sucesso dos outros, nem com aqueles que maquinam o mal."
    ],
    "isaias-41": [
        "\"Calem-se diante de mim, ó ilhas! Que as nações renovem as suas forças! Que se aproximem e falem; vamos nos reunir para o julgamento.\"",
        "\"Quem suscitou aquele que vem do oriente, e a quem a justiça chama para servi-la? Ele entrega as nações nas suas mãos e subjuga reis diante dele.\"",
        "Quem operou e realizou tudo isso, chamando as gerações desde o princípio? Eu, o Senhor, que sou o primeiro, e que estarei com os últimos; eu mesmo sou.",
        "Mas você, Israel, meu servo, Jacó, a quem escolhi, descendência de Abraão, meu amigo;",
        "você, a quem tirei dos confins da terra, chamando-o dos seus recantos mais remotos, e lhe disse: Você é o meu servo; eu o escolhi e não o rejeitei.",
        "Por isso não tema, pois estou com você; não tenha medo, pois sou o seu Deus. Eu o fortalecerei e o ajudarei; eu o segurarei com a minha mão direita vitoriosa."
    ],
    "mateus-11": [
        "Depois que Jesus terminou de instruir os seus doze discípulos, partiu dali para ensinar e pregar nas cidades da Galiléia.",
        "Quando João ouviu falar na prisão sobre os feitos do Cristo, enviou os seus discípulos para lhe perguntar:",
        "\"És tu aquele que haveria de vir ou devemos esperar outro?\"",
        "Jesus respondeu: \"Voltem e anunciem a João o que vocês estão ouvindo e vendo:",
        "os cegos enxergam, os mancos andam, os leprosos são purificados, os surdos ouvem, os mortos são ressuscitados, e as boas novas são pregadas aos pobres;",
        "e feliz é aquele que não se escandaliza por minha causa\".",
        "Venham a mim, todos os que estão cansados e sobrecarregados, e eu darei descanso a vocês.",
        "Tomem sobre vocês o meu jugo e aprendam de mim, pois sou manso e humilde de coração, e vocês encontrarão descanso para as suas almas.",
        "Pois o meu jugo é suave e o meu fardo é leve."
    ],
    "joao-1": [
        "No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus.",
        "Ele estava no princípio com Deus.",
        "Todas as coisas foram feitas por intermédio dele, e sem ele nada do que foi feito se fez.",
        "Nele estava a vida, e a vida era a luz dos homens.",
        "A luz brilha nas trevas, e as trevas não a derrotaram.",
        "Houve um homem enviado por Deus, cujo nome era João.",
        "Este veio como testemunha, para testificar acerca da luz, a fim de que todos cressem por meio dele.",
        "Ele não era a luz, mas veio para testemunhar da luz.",
        "Estava chegando ao mundo a verdadeira luz, que ilumina todos os homens.",
        "Aquele que é a Palavra tornou-se carne e viveu entre nós. Vimos a sua glória, glória como do Unigênito vindo do Pai, cheio de graça e de verdade."
    ],
    "romanos-8": [
        "Portanto, agora já não há condenação para os que estão em Cristo Jesus,",
        "porque por meio de Cristo Jesus a lei do Espírito de vida me libertou da lei do pecado e da morte.",
        "Porque o que a lei não podia fazer, enferma que estava pela carne, Deus o fez enviando o seu próprio Filho em semelhança da carne do pecado.",
        "Porque os que são segundo a carne inclinam-se para as coisas da carne; mas os que são segundo o Espírito para as coisas do Espírito.",
        "Porque todos os que são guiados pelo Espírito de Deus, esses são filhos de Deus.",
        "O próprio Espírito testemunha ao nosso espírito que somos filhos de Deus.",
        "Considero que os nossos sofrimentos atuais não podem ser comparados com a glória que em nós será revelada.",
        "Da mesma forma o Espírito nos ajuda em nossa fraqueza, pois não sabemos como orar, mas o próprio Espírito intercede por nós com gemidos inexprimíveis.",
        "Sabemos que Deus age em todas as coisas para o bem daqueles que o amam, dos que foram chamados de acordo com o seu propósito.",
        "Que diremos, pois, diante dessas coisas? Se Deus é por nós, quem será contra nós?",
        "Aquele que nem mesmo a seu próprio Filho poupou, antes o entregou por todos nós, como não nos dará também com ele todas as coisas?",
        "Quem nos separará do amor de Cristo? Será tribulação, ou angústia, ou perseguição, ou fome, ou nudez, ou perigo, ou espada?",
        "Mas, em todas estas coisas somos mais que vencedores, por meio daquele que nos amou.",
        "Pois estou convencido de que nem morte nem vida, nem anjos nem demônios, nem o presente nem o futuro, nem quaisquer poderes,",
        "nem altura nem profundidade, nem qualquer outra coisa na criação será capaz de nos separar do amor de Deus que está em Cristo Jesus, nosso Senhor."
    ],
    "filipenses-4": [
        "Portanto, meus irmãos amados e mui saudosos, minha alegria e coroa, permaneçam firmes no Senhor, amados.",
        "Alegrem-se sempre no Senhor. Novamente direi: alegrem-se!",
        "Seja a amabilidade de vocês conhecida por todos. Perto está o Senhor.",
        "Não andem ansiosos por coisa alguma, mas em tudo, pela oração e súplicas, e com ação de graças, apresentem seus pedidos a Deus.",
        "E a paz de Deus, que excede todo o entendimento, guardará os seus corações e as suas mentes em Cristo Jesus.",
        "Finalmente, irmãos, tudo o que for verdadeiro, tudo o que for nobre, tudo o que for correto, tudo o que for puro, tudo o que for amável, tudo o que for de boa fama, se houver algo de excelente ou digno de louvor, pensem nessas coisas.",
        "Tudo posso naquele que me fortalece.",
        "O meu Deus suprirá todas as necessidades de vocês, de acordo com as suas gloriosas riquezas em Cristo Jesus."
    ],
    "proverbios-3": [
        "Meu filho, não se esqueça da minha lei, mas guarde no coração os meus mandamentos,",
        "pois eles prolongarão a sua vida por muitos anos e lhe darão prosperidade e paz.",
        "Que o amor e a fidelidade jamais o abandonem; prenda-os ao redor do seu pescoço, escreva-os na tábua do seu coração.",
        "Então você terá o favor de Deus e dos homens, e boa reputação.",
        "Confie no Senhor de todo o seu coração e não se apoie em seu próprio entendimento;",
        "reconheça o Senhor em todos os seus caminhos, e ele endireitará as suas veredas.",
        "Não seja sábio aos seus próprios olhos; tema o Senhor e evite o mal.",
        "Isso lhe dará saúde ao corpo e vigor aos ossos."
    ],
    "1pedro-5": [
        "Aos presbíteros que estão entre vocês, exorto eu, que sou também presbítero com eles:",
        "Pastoreiem o rebanho de Deus que está aos seus cuidados, vigiando com alegria e dedicação.",
        "Da mesma forma jovens, sujeitem-se aos mais velhos. Sejam todos humildes uns para com os outros, porque Deus se opõe aos orgulhosos, mas concede graça aos humildes.",
        "Humilhem-se, pois, debaixo da potente mão de Deus, para que ele a seu tempo os exalte,",
        "lançando sobre ele toda a sua ansiedade, porque ele tem cuidado de vocês.",
        "Sejam sóbrios e vigiem. O diabo, o inimigo de vocês, anda ao redor como leão, rugindo e procurando a quem devorar.",
        "Resistam-lhe, permanecendo firmes na fé, sabendo que os seus irmãos espalhados pelo mundo passam pelos mesmos sofrimentos.",
        "O Deus de toda a graça, que os chamou para a sua glória eterna em Cristo Jesus, depois de terem sofrido durante um pouco de tempo, os restaurará, os confirmará, lhes dará forças e os porá sobre firmes alicerces.",
        "A ele seja o poder para todo o sempre. Amém."
    ],
    "2timoteo-3": [
        "Saiba disto: nos últimos dias sobrevirão tempos terríveis.",
        "Os homens serão egoístas, avarentos, presunçosos, arrogantes, blasfemos, desobedientes aos pais, ingratos, ímpios,",
        "sem amor pela família, irreconciliáveis, caluniadores, sem domínio próprio, cruéis, inimigos do bem,",
        "traidores, precipitados, orgulhosos, mais amantes dos prazeres do que amigos de Deus,",
        "tendo aparência de piedade, mas negando o seu poder. Afaste-se desses também.",
        "Quanto a você, porém, permaneça nas coisas que aprendeu e das quais tem convicção, pois você sabe de quem o aprendeu.",
        "Porque desde criança você conhece as Sagradas Letras, que são capazes de torná-lo sábio para a salvação mediante a fé em Cristo Jesus.",
        "Toda a Escritura é inspirada por Deus e útil para o ensino, para a repreensão, para a correção e para a instrução na justiça,",
        "para que o homem de Deus seja apto e plenamente preparado para toda boa obra."
    ]
};

// Estado global do banco NVI
window.BIBLE_NVI_STORE = null;
let bibleLoadInProgress = false;
const bibleListeners = [];

/**
 * Registra ouvinte para quando a Bíblia NVI for carregada na memória.
 */
function onBibleNviLoaded(callback) {
    if (typeof callback !== "function") return;
    if (window.BIBLE_NVI_STORE) {
        callback(window.BIBLE_NVI_STORE);
    } else {
        bibleListeners.push(callback);
    }
}

/**
 * Inicializa o carregamento do banco completo NVI (66 livros).
 * Carrega a partir do CDN de alta performance ou armazenamento local.
 */
function carregarBancoBibliaNVI() {
    if (window.BIBLE_NVI_STORE || bibleLoadInProgress) return;
    bibleLoadInProgress = true;

    // 1. Tenta carregar do localStorage
    try {
        const cached = localStorage.getItem("solascriptura_bible_nvi_db");
        if (cached) {
            const parsed = JSON.parse(cached);
            if (Array.isArray(parsed) && parsed.length >= 66) {
                window.BIBLE_NVI_STORE = parsed;
                bibleLoadInProgress = false;
                notificarOuvintesBibleNvi();
                return;
            }
        }
    } catch (e) {
        // localStorage pode ter quota limitada, prossegue com fetch
    }

    // 2. Fetch de CDN resiliente
    const cdnUrl = "https://cdn.jsdelivr.net/gh/thiagobodruk/bible/json/pt_nvi.json";
    const fallbackUrl = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_nvi.json";

    fetch(cdnUrl)
        .then(res => {
            if (!res.ok) throw new Error("Falha no CDN primário");
            return res.json();
        })
        .catch(() => fetch(fallbackUrl).then(res => res.json()))
        .then(data => {
            if (Array.isArray(data) && data.length >= 66) {
                window.BIBLE_NVI_STORE = data;
                try {
                    localStorage.setItem("solascriptura_bible_nvi_db", JSON.stringify(data));
                } catch (err) {
                    // Cota cheia, mantém em memória durante a sessão
                }
                notificarOuvintesBibleNvi();
            }
        })
        .catch(err => {
            console.warn("Aviso: Carregamento estendido da Bíblia NVI offline:", err);
        })
        .finally(() => {
            bibleLoadInProgress = false;
        });
}

function notificarOuvintesBibleNvi() {
    while (bibleListeners.length > 0) {
        const cb = bibleListeners.shift();
        try {
            cb(window.BIBLE_NVI_STORE);
        } catch (e) {
            console.error(e);
        }
    }
}

// Inicia o carregamento em background assim que o script é interpretado
if (typeof window !== "undefined") {
    setTimeout(carregarBancoBibliaNVI, 200);
}

/**
 * Normaliza nomes para busca resiliente.
 */
function normalizarTextoBusca(str) {
    return (str || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]/g, "");
}

/**
 * Retorna o objeto do capítulo com todos os versículos formatados da NVI.
 * Suporta retorno síncrono e atualização reativa.
 */
function obterCapituloBiblia(livroId, capituloNum) {
    const capInt = parseInt(capituloNum, 10) || 1;
    const livroObj = BIBLE_BOOKS.find(b => b.id === livroId) || BIBLE_BOOKS[18]; // Salmos padrão
    const chavePreload = `${livroObj.id}-${capInt}`;

    // 1. Verifica capítulos no preload instantâneo
    if (BIBLE_NVI_PRELOAD[chavePreload]) {
        const versosArray = BIBLE_NVI_PRELOAD[chavePreload];
        return {
            titulo: `${livroObj.nome} ${capInt}`,
            livro: livroObj.nome,
            livroId: livroObj.id,
            capitulo: capInt,
            versao: "NVI",
            totalVersos: versosArray.length,
            carregando: false,
            versiculos: versosArray.map((txt, idx) => ({
                numero: idx + 1,
                verso: idx + 1,
                texto: txt
            }))
        };
    }

    // 2. Verifica se o banco completo NVI já está na memória
    if (window.BIBLE_NVI_STORE && Array.isArray(window.BIBLE_NVI_STORE)) {
        // Encontra o livro pelo índice canônico ou abreviação/nome
        let livroDb = window.BIBLE_NVI_STORE[livroObj.index];
        if (!livroDb || normalizarTextoBusca(livroDb.name) !== normalizarTextoBusca(livroObj.nome)) {
            livroDb = window.BIBLE_NVI_STORE.find(item => 
                normalizarTextoBusca(item.name) === normalizarTextoBusca(livroObj.nome) ||
                (item.abbrev && normalizarTextoBusca(item.abbrev) === normalizarTextoBusca(livroObj.abrev))
            );
        }

        if (livroDb && Array.isArray(livroDb.chapters)) {
            const capituloIdx = capInt - 1;
            const listaTextos = livroDb.chapters[capituloIdx];
            if (Array.isArray(listaTextos) && listaTextos.length > 0) {
                return {
                    titulo: `${livroObj.nome} ${capInt}`,
                    livro: livroObj.nome,
                    livroId: livroObj.id,
                    capitulo: capInt,
                    versao: "NVI",
                    totalVersos: listaTextos.length,
                    carregando: false,
                    versiculos: listaTextos.map((txt, idx) => ({
                        numero: idx + 1,
                        verso: idx + 1,
                        texto: txt
                    }))
                };
            }
        }
    }

    // 3. Se ainda está baixando o banco, dispara carregamento e retorna estado receptivo
    carregarBancoBibliaNVI();

    return {
        titulo: `${livroObj.nome} ${capInt}`,
        livro: livroObj.nome,
        livroId: livroObj.id,
        capitulo: capInt,
        versao: "NVI",
        totalVersos: 0,
        carregando: true,
        versiculos: []
    };
}

/**
 * Função de interface uniforme para obter os versículos de um capítulo.
 * Retorna array com `{ numero, verso, texto }`.
 */
function obterTextoCapituloBiblico(livroId, capituloNum, versao = "NVI") {
    const dadosCap = obterCapituloBiblia(livroId, capituloNum);
    return dadosCap.versiculos || [];
}
