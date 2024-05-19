
import React, { useState } from 'react';
import { css } from '@emotion/css';
import { useQuery } from '@tanstack/react-query';

import SearchBar from '../../components/SearchBar';
import axiosInstance from '../../axios';
import { CircularProgress } from '@mui/material';


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

`;

const HomePage: React.FC  = () => {
  const [searchQuery, setSearchQuery] = useState<string>('');

  const onSearchTriggered = (query: string) => {
    setSearchQuery(query);
  };

   const { isLoading, data } = useQuery({
    queryKey: ['getArticles', searchQuery],
    queryFn: () => axiosInstance.get('/', {params: {query: searchQuery}}).then((res) => res.data),
    enabled: !!searchQuery
  })

  return (
    <div className={homePageWrapper}>
      <div className={homePageTitleRow}>
        <h1>Intelligent Research Assistant</h1>
        <SearchBar onSearchTriggered={onSearchTriggered}  />
      </div>

      <div className={articlesListSectionWrapper}>
        {isLoading ? (<CircularProgress />) : (<>{JSON.stringify(data)}</>)}
      </div>
    </div>
  );
}

export default HomePage;