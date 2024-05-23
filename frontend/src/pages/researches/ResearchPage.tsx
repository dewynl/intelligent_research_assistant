import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import axiosInstance from '../../axios';
import Loading from '../../components/Loading';
import { Box, Card, CardContent, Chip, Link, List, ListItem, ListItemText, Typography } from '@mui/material';
import { css } from '@emotion/css';

const pageContainer = css`
  display: flex;
  flex-direction: column;
  padding: 24px;
`;

const topRowContainerStyles = css`
  display: flex;
  flex-direction: row;
  gap: 16px;
`;

const ResearchPage = () => {
  const { researchId } = useParams();
  const [research, setResearch] = useState<any>(undefined);

  const { isLoading, error, data } = useQuery({
    queryKey: ['getResearch', researchId],
    queryFn: () => axiosInstance.get(`/research/${researchId}`).then((res) => res.data),
    refetchInterval: 5000,
  });

  useEffect(() => {
    if (data) {
      setResearch(data);
    }
  }, [data]);
 
  if (isLoading) {
    return (
      <Loading />
    );
  };
  
  if (error) return <div>Error: {error?.message}</div>;

  return (
    <div className={pageContainer}>
      <Typography variant="h4" gutterBottom>
        Research Details
      </Typography>

      <div className={topRowContainerStyles}>
        <Card>
          <CardContent>
            <Typography>
              <strong>Research ID:</strong> {research?.id}
            </Typography>
            <Typography>
              <strong>Category:</strong> {research?.research_category}
            </Typography>
            <Typography>
              <strong>Keywords:</strong>{' '}
              {research?.keywords.map((keyword: string) => (
                <Chip key={keyword} label={keyword} size="small" sx={{ mr: 1 }} />
              ))}
            </Typography>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Summary
            </Typography>
            <Typography>{research?.summary}</Typography>
          </CardContent>
        </Card>
      </div>

      <Box mt={4}>
        <Typography variant="h5" gutterBottom>
          Related Articles
        </Typography>
        {research?.articles.map((article: any) => (
          <Card key={article.id} sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6">{article.title}</Typography>
              <Typography>
                <strong>Abstract:</strong> {article.abstract}
              </Typography>
              <Typography>
                <strong>Link:</strong>{' '}
                <Link href={article.link} target="_blank" rel="noopener noreferrer">
                  {article.link}
                </Link>
              </Typography>
              <Typography>
                <strong>DOI:</strong> {article.doi}
              </Typography>
              <Typography>
                <strong>PDF URL:</strong>{' '}
                <Link href={article.pdf_url} target="_blank" rel="noopener noreferrer">
                  {article.pdf_url}
                </Link>
              </Typography>
              <Typography>
                <strong>Source:</strong> {article.source}
              </Typography>
              <Typography>
                <strong>Source ID:</strong> {article.source_id}
              </Typography>
              <Box mt={2}>
                <Typography>
                  <strong>Authors:</strong>
                </Typography>
                <List dense>
                  {article.authors.map((author: any) => (
                    <ListItem key={author.id}>
                      <ListItemText primary={author.name} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            </CardContent>
          </Card>
        ))}
      </Box>
    </div>
  );
};

export default ResearchPage;