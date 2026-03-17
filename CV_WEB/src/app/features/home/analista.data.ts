import { Curriculum } from '../../models/curriculum.model';


export const HOME_ANALISTA: Curriculum = {
  personalInfo: {
    photo: 'assets/images/foto_rodrigo.jpg',
    name: 'Rodrigo Barros de Matos',
    maritalStatus: 'Solteiro',
    birthDate: '1984-08-03',
    address: 'Av. Água Verde, 1.575 - Água Verde - Curitiba, PR',
    title: 'Analista de Dados',
    email: 'rbmgestao@gmail.com',
    phone: '+55 41 99911-4530',
    linkedin: 'www.linkedin.com/in/rodrigo-matos-747b40116',
    github: 'https://github.com/MSM-Analytics/Portfolio/tree/main'
  },


  summary: 'Analista de Dados com mais de 12 anos de experiência em consultoria empresarial, atuando na análise de processos, definição de KPIs e desenvolvimento de relatórios estratégicos para melhoria de desempenho e redução de custos. Experiência em ETL, modelagem e visualização de dados com Power BI, além de tratamento e análise utilizando SQL e Python. Possuo forte visão de negócio, capacidade analítica e habilidade em transformar dados em insights claros para apoiar a tomada de decisão e otimização de resultados.',

  skills: [
    {
      category: 'POWER BI',
      items: ['ETL/ELT', 'Modelagem de dados', 'Linguagem M', 'Linguagem DAX', 'Data Storytelling', 'Análise Exploratória', 'Insights']
    },
    {
      category: 'Python',
      items: ['Pandas', 'NunPy', 'Matchplotlib', 'SQL Alchemy']
    },
    {
      category: 'SQL',
      items: ['Tratamento de dados', 'Query', 'View', 'Join']
    },
    {
      category: 'Ferramentas',
      items: ['Figma', 'Data Brix', 'Power BI', 'Chat GPT']
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
}
