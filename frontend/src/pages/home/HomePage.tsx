
import React, { useEffect, useState } from 'react';
import { useNavigate } from "react-router-dom";
import { css } from '@emotion/css';
import { useMutation, useQuery } from '@tanstack/react-query';

import SearchBar from '../../components/SearchBar';
import axiosInstance from '../../axios';
import { CircularProgress } from '@mui/material';
import ArticleListItem from './ArticleListItem';
import { Article } from '../../schemas';
import Snackbar from './Snackbar';


const homePageWrapper = css`
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 32px;
`;

const homePageTitleRow = css`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const articlesListSectionWrapper = css`
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
  align-items: center;
`;

const HomePage: React.FC  = () => {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedArticleIds, setSelectedArticleIds] = useState<string[]>([]);
  const navigate = useNavigate();

  const onSearchTriggered = (query: string) => {
    setSearchQuery(query);
    setSelectedArticleIds([]);
  };

  const { isLoading: areArticlesLoading, data } = useQuery({
    queryKey: ['getArticles', searchQuery],
    queryFn: () => axiosInstance.get('/search/arxiv', {params: {query: searchQuery}}).then((res) => res.data),
    enabled: !!searchQuery
  })
  
  const saveArticles = useMutation({
    mutationFn: (articleIds: string[]) => {
      return axiosInstance.post('/extract/arxiv',  articleIds)
    }
  })

  const handleArticleSelection = (articleId: string, isSelected: boolean) => {
    if (isSelected) {
      setSelectedArticleIds([...selectedArticleIds, articleId]);
    } else {
      setSelectedArticleIds(selectedArticleIds.filter((id) => id !== articleId));
    }
  };

  const saveSelectedArticles = () => {
    saveArticles.mutate(selectedArticleIds);
  }

  const articles = data || [];

  const isLoading = areArticlesLoading || saveArticles.isPending;

  useEffect(() => {
    if (saveArticles.isSuccess) {
      navigate('/researches');
    }
  }, [saveArticles.isSuccess])

  return (
    <div className={homePageWrapper}>
      <div className={homePageTitleRow}>
        <h1>Intelligent Research Assistant</h1>
        <SearchBar onSearchTriggered={onSearchTriggered}  />
      </div>

      <div className={articlesListSectionWrapper}>
        {isLoading ? <CircularProgress /> : 
        (
          <>
            {articles.map((article: Article) => (
              <ArticleListItem 
                key={article.id} 
                article={article} onSelect={handleArticleSelection}
                isSelected={selectedArticleIds.includes(article.id)} 
              />
            ))}
          </>
        )}
      </div>
      {selectedArticleIds.length > 0 && (
        <Snackbar 
          text={`${selectedArticleIds.length} article(s) selected`} 
          onActionLabel='Process articles' 
          onActionClicked={saveSelectedArticles}
        />
      )}
    </div>
  );
}

export default HomePage;