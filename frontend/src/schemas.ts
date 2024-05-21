
export interface Article {
  id: string;
  title: string;
  authors: string[];
  abstract: string;
  categories: string[]
  link: string
  doi: string | undefined
  pdf_url: string | undefined
}