import React from 'react';

import { Article } from '../../schemas';
import { Checkbox, Link } from '@mui/material';
import { css } from '@emotion/css';

const articleListItemCotnainerStyles = css`
  width: 100%;	
`;

const titleRowStyles = css`
  display: flex;
  flex-direction: row;
  gap: 8px;
`;

const ArticleListItem = ({
  article,
  isSelected,
  onSelect,
}: {
  article: Article;
  isSelected: boolean;
  onSelect: (articleId: string, isSelected: boolean) => void;
}) => {
  const { title, authors, abstract, categories, link, doi, pdf_url} = article;

  const onChange = () => {
    onSelect(article.id, !isSelected);
  };


  return (
    <div className={articleListItemCotnainerStyles}>
      <div className={titleRowStyles}>
        <Checkbox checked={isSelected} onChange={onChange} />
        <Link href={link} target="_blank" rel="noreferrer">
          <h3>{title}</h3>
        </Link>
      </div>
      <div>
        <p>
          {authors.join(', ')} - {categories.join(', ')}
        </p>
        <p>{abstract}</p>
        {doi && <p>DOI: {doi}</p>}
        {pdf_url && (
          <Link href={pdf_url} target="_blank" rel="noreferrer">
            <p>Open PDF</p>
          </Link>
        )}
      </div>
    </div>
  );
};

export default ArticleListItem;