import React, { useEffect, useState } from 'react';
import { css } from '@emotion/css';
import { useQuery } from '@tanstack/react-query';
import axiosInstance from '../../axios';
import { CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Loading from '../../components/Loading';

const styles = {
  container: css`
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  `,
  list: css`
    list-style-type: none;
    padding: 0;
  `,
  listItem: css`
    background-color: #f5f5f5;
    border-radius: 4px;
    padding: 10px;
    margin-bottom: 10px;
  `,
  clickable: css`
    cursor: pointer;
    transition: background-color 0.3s;
    &:hover {
      background-color: #e0e0e0;
    }
  `,
  research: css`
    display: flex;
    justify-content: space-between;
    align-items: center;
  `,
  researchId: css`
    font-weight: bold;
  `,
  researchStatus: css`
    color: #666;
  `,
};

const Researches = () => {
  const navigate = useNavigate();
  const [researches, setResearches] = useState<any[]>([])

  const { isLoading, error, data } = useQuery({
    queryKey: ['getResearches'],
    queryFn: () => axiosInstance.get('/researches').then((res) => res.data),
    refetchInterval: 2000,
  });

  const handleResearchClick = (researchId: string) => {
    navigate(`/researches/${researchId}`);
  };

  useEffect(() => {
    setResearches(data)
  }, [data])

  if (isLoading) {
    return (
      <Loading />
    );
  };

  if (!researches || error) return <div>Error: {error?.message}</div>;

  return (
    <div className={styles.container}>
      <h2>Research List</h2>
      <ul className={styles.list}>
        {researches.map((research: any) => (
          <li
            key={research.id}
            className={`${styles.listItem} ${styles.clickable}`}
            onClick={() => handleResearchClick(research.id)}
          >
            <div className={styles.research}>
              <span className={styles.researchId}>Research ID: {research.id}</span>
              <span className={styles.researchStatus}>
                Status: {research.research_preprocess_status}
              </span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Researches;