import { DataPortfolioItem } from '../../models/curriculum.model';

export const PORTFOLIO_DATA_JS: DataPortfolioItem[] = [
  {
    id: 'automotivo',
    title: 'Site Automotivo',
    description: 'Landing page para loja de carros importados.',
    projectPath: 'automotivo',
    thumbnail: 'assets/images/site-automotivo.png',
    tags: ['HTML', 'SCSS', 'JS', 'Responsivo']
  },

  {
    id: 'cafeteria',
    title: 'Site Cafeteria',
    description: 'E commerce institucional com menu para um ciber café.',
    projectPath: 'cafeteria',
    thumbnail: 'assets/images/site-cafeteria.png',
    tags: ['E commerce', 'HTML', 'CSS', 'JS', 'Responsivo', 'Carrinho de compras']
  },

  {
    id: 'bebidas',
    title: 'Slider Bebidas',
    description: 'Carrocel slider promocional para marca de bebidas.',
    projectPath: 'bebidas',
    thumbnail: 'assets/images/site-bebidas.png',
    tags: ['Landing Page', 'HTML', 'CSS', 'JS', 'Responsivo']
  }
];