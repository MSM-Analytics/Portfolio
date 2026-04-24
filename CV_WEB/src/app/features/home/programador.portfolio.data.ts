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
    description: 'Website institucional com menu para um ciber café.',
    projectPath: 'cafeteria',
    thumbnail: 'assets/images/site-cafeteria.png',
    tags: ['HTML', 'CSS', 'JS', 'Responsivo']
  },

  {
    id: 'bebidas',
    title: 'slider Bebidas',
    description: 'Landing page promocional para marca de bebidas.',
    projectPath: 'bebidas',
    thumbnail: 'assets/images/site-bebidas.png',
    tags: ['Landing Page', 'HTML', 'CSS', 'JS', 'Responsivo']
  }
];