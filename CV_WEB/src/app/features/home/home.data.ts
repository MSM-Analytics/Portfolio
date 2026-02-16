import { Curriculum } from '../../models/curriculum.model';


export const HOME_DATA: Curriculum = {
  personalInfo: {
    photo: 'assets/images/foto_rodrigo.jpg',
    name: 'Rodrigo Barros de Matos',
    title: 'Programador Web',
    email: 'rbmgestao@gmail.com',
    phone: '+55 41 99911-4530',
    location: 'Curitiba, PR - Brasil',
    linkedin: 'https://www.linkedin.com/in/rodrigo-matos-747b40116',
    github: 'https://github.com/MSM-Analytics'
  },


  summary: 'Programador Web com experiência acadêmica nas seguintes linguagens, Angular, React, Python, Java, PHP, SQL, HTML e CSS. Busco constantemente aprender novas tecnologias e aplicar as melhores práticas de desenvolvimento para criar soluções eficientes e escaláveis. Busco uma oportunidade de colocar em prática todo o conhecimento acadêmico adiquirido e alcançar o objetivo de migrar para carreira de programador',

  skills: [
    {
      category: 'Frontend',
      items: ['Angular', 'React', 'TypeScript', 'JavaScript', 'HTML5', 'CSS3', 'Tailwind CSS', 'Bootstrap']
    },
    {
      category: 'Backend',
      items: ['Python', 'Java', 'PHP']
    },
    {
      category: 'Banco de Dados',
      items: ['PostgreSQL', 'MySQL', 'Firebird']
    },
    {
      category: 'Ferramentas',
      items: ['VS Code', 'Git', 'Github', 'Squarespace', 'Figma', 'Slack', 'Data Brix', 'Power BI', 'Docker', 'Chat GPT']
    },
    {
      category: 'Soft Skills',
      items: ['Trabalho em Equipe', 'Liderança', 'Comunicação', 'Resolução de Problemas', 'Metodologias Ágeis', 'Raciocínio Lógico']
    }
  ],

  experiences: [
    {
      position: 'Consultor Sênior',
      company: 'Supplant Consultoria',
      location: 'São Paulo, SP',
      startDate: 'Mai 2018',
      endDate: 'Out 2025',
      current: false,
      description: [
        'Análise Operacional;',
        'Propostas de melhorias visando redução de custos e aumento de produtividade;',
        "implantação de KPI's;",
        'Desenvolvimento de relatórios de gestão operacional;',
        'Implantação de sistema de gestão (Reuniões entre superiores e seus subordinados em todos os níveis da hierarquia);',
        'Desenvolvimento de planos de ação para corrigir desvios;',
        'Acompanhamento e suporte técnico no desenvolvimento e na execução dos planos de ação.',
        'Implantação de sistema de manutenção ENGEMAN;',
        'Implantação de setor da Manutenção PCM;',
        'Implementação de Sistema de vendas ATACK;',
        'Estruturação de carteiras comerciais;',
        'Implantação de setor de televendas;',
        'Trinamento de vendedores;',
        'Análise de clientes (frequencia de compras, volume comprado)',
        'Análise de rotas (Frequencia de entrega, volume carregado, custo logísco)',
        'Reestruturação de rotas (Visando redução de custo logísco)',
      ]
    },
    {
      position: 'Consultor Pleno',
      company: 'Supplant Consultoria',
      location: 'São Paulo, SP',
      startDate: 'Mar 2012',
      endDate: 'Dez 20218',
      current: false,
      description: [
        'Análise Operacional;',
        'Propostas de melhorias visando reduçã de custos e aumento de produvidade;',
        'Implantação de relatórios operacionais;',
        "implantação de KPI's;",
        'Implantação de sistema de gestão (Reuniões entre superiores e seus subordinados em todos os níveis da hierarquia);',
        'Cronoalnálise e definição de capacidade produva;',
        'Balanceamento de linha produva;',
        'Desenvolvimento de planos de ação para corrigir desvios;',
        'Acompanhamento e suporte técnico no desenvolvimento dos planos de ação.'
      ]
    },
  ],

  education: [
    {
      degree: 'Bacharelado em Adminsração de Empresas',
      institution: 'Universidade Tuiuti do Paraná (UTP)',
      location: 'Curitiba, PR',
      startDate: '2008',
      endDate: '2012',
      description: [
        'Curso de graduação em administração de empresas'
      ]
    },
    {
      degree: 'Curso Técnico em Programação Web',
      institution: 'SENAC Portão',
      location: 'Curitiba, PR',
      startDate: '2021',
      endDate: '2021',
      description: [
        'HTML',
        'CSS',
        'PHP introdução - CRUD'
      ]
    },
    {
      degree: 'Curso Técnico em Programação Web',
      institution: 'Alura',
      location: 'Online',
      startDate: '2022',
      endDate: '2022',
      description: [
        'Python',
        'PHP - Láravel',
        'Java Web',
      ]
    },
    {
      degree: 'Curso Técnico em Análise de Dados',
      institution: 'Xperiun',
      location: 'Online',
      startDate: '2023',
      endDate: '2026',
      description: [
        'ETL - Extração, tratamento e carregamento de dados;',
        'Modelagem de dados;',
        'Design de Dadhboards;',
        'Data storey telling;',
        'SQL;',
        'PYTHON;',
        'Power BI;',
        'Data Brix',
        'DAX',
        'Linguagem M'
      ]
    }
  ]
};
