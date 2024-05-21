import React from 'react';
import { css } from '@emotion/css';

import {  IconButton, Input } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

const containerStyles = css`
  display: flex;
  flex-direction: row;
  width: 100%;
  justify-content: center;
`;

const inputStyles = css`
  width: 800px;
`;

interface SearchBarProps {
  onSearchTriggered: (query: string) => void;
}

const SearchBar = ({onSearchTriggered, ...props}: SearchBarProps) => { 
  const [search, setSearch] = React.useState('');

  return (
    <div className={containerStyles}>
      <>
        <Input type='text' className={inputStyles} placeholder='Search' onChange={(e) => setSearch(e.target.value)} 
          onKeyDown={(event) => {
              if (event.key === 'Enter') {
               onSearchTriggered(search)
              }
            }}
          />
        <IconButton onClick={() => onSearchTriggered(search)} >
          <SearchIcon />
        </IconButton>
      </>

      <>
      
      </>
    </div>
  );
}

export default SearchBar;