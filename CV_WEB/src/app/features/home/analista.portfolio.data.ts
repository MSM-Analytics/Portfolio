import { DataPortfolioItem } from '../../models/curriculum.model';

export const PORTFOLIO_DATA: DataPortfolioItem[] = [
  {
    id: 'Logistica-Transporte',
    title: 'Análise de Transporte',
    description: 'Análise de transporte por filial, comparativo entre períodos e tipo de veículo.',
    embedUrl: 'https://app.powerbi.com/view?r=eyJrIjoiZDQ3NWIxYjktZTRiZS00YTM4LWI5N2EtZDJiNDEzM2Y0YTMxIiwidCI6ImE4N2RmYjBlLTI0YzYtNDYyOC1iMjkyLWQ2ZDlhODkxMmUwYiJ9',
    thumbnail: 'assets/images/dash_log.png',
    tags: ['Receita', 'Custo', 'Margem', 'Comparativos', 'OTIF', 'ON TIME', 'IN FULL']
  },
  {
    id: 'Comercial',
    title: 'Dashboard de Vendas',
    description: 'Análise de faturamento e atingimento de metas global, por equipe e por produto.',
    embedUrl: 'https://app.powerbi.com/view?r=eyJrIjoiYzAyZDEyNzQtYzhhMi00ZDg1LTg1YTUtNTU0NzVhMTM2Njg2IiwidCI6ImE4N2RmYjBlLTI0YzYtNDYyOC1iMjkyLWQ2ZDlhODkxMmUwYiJ9',
    thumbnail: 'assets/images/dash_vdas.png',
    tags: ['Faturamento', 'Margem', 'Ticket Médio', 'Fat. vs Meta', 'Comparativos']
  },
  {
    id: 'Industrial',
    title: 'Dashboard Industrial',
    description: 'Monitoramento Industrial com foco em produtividade por equipamento e operador.',
    embedUrl: 'https://app.powerbi.com/view?r=eyJrIjoiMmIzZDYxMmYtZmNjMC00MzM2LTk5YzgtN2IwMDNlNDZiMTVhIiwidCI6ImE4N2RmYjBlLTI0YzYtNDYyOC1iMjkyLWQ2ZDlhODkxMmUwYiJ9',
    thumbnail: 'assets/images/dash_ind.png',
    tags: ['OEE', 'Produtividade', 'Qualidade', 'Disponibilidade', 'Análise de Falhas' ]
  }
];