export interface Curriculum {
  personalInfo: PersonalInfo;
  summary: string;
  cards?: CardItem[];
  experiences?: Experience[];
  education?: Education[];
  skills?: Skill[];
}

export interface PersonalInfo {
  photo?: string;
  name: string;
  maritalStatus?: string;
  birthDate?: string;
  address?: string;
  title?: string;
  email: string;
  phone: string;
  linkedin?: string;
  github?: string;
  website?: string;
}

export interface Experience {
  position: string;
  company: string;
  location: string;
  startDate: string;
  endDate: string;
  current: boolean;
  description: string[];
}

export interface Education {
  degree: string;
  institution: string;
  location: string;
  startDate: string;
  endDate: string;
  description: string[];
}

export interface Skill {
  category: string;
  items: string[];
}

export interface CardItem {
  title: string;
  description: string;
  route: 'programador' | 'analista';
  image?: string;
}

export interface DataPortfolioItem {
  id: string;
  title: string;
  description: string;
  embedUrl?: string;
  projectPath?: string;
  thumbnail?: string;
  tools?: string[];
  tags?: string[];
  dataset?: string;
  createdAt?: string;
}