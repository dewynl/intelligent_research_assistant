import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import axiosInstance from '../../axios';
import Loading from '../../components/Loading';
import { Box, Card, CardContent, Chip, Grid, Link, List, ListItem, ListItemText, Typography } from '@mui/material';
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
  const [relatedArticles, setRelatedArticles] = useState<[]>([]);

  const { isLoading, error, data } = useQuery({
    queryKey: ['getResearch', researchId],
    queryFn: () => axiosInstance.get(`/research/${researchId}`).then((res) => res.data),
  });

  const { isLoading: areCategoriesLoading, data: inferredCategories } = useQuery({
    queryKey: ['getResearchInferredCategories', researchId],
    queryFn: () => axiosInstance.get(`/research/${researchId}/inferred-categories`).then((res) => res.data),
  });

  useEffect(() => {
    if (data) {
      setResearch(data);
    }
  }, [data]);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws');

    socket.onopen = () => {
      console.log('Connected to the server')
      socket.send(JSON.stringify({ research_id: researchId }));
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.related_articles) {
        setRelatedArticles(data.related_articles);
      }
    };

    return () => {
      console.log('Disconnected from the server')
      socket.close();
    };
  }, [researchId]);

  if (isLoading || areCategoriesLoading) {
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

      {inferredCategories && (
        <Box mt={4}>
        <Typography variant="h5" gutterBottom>
          Inferred Categories
        </Typography>
        <Grid container spacing={2}>
          {Object.entries(inferredCategories).map(([category, percentage]) => (
            <Grid item xs={12} sm={6} md={4} key={category}>
              <Card>
                <CardContent>
                  <Typography variant="h6">{category.replace(/_/g, ' ')}</Typography>
                  <Typography variant="body1">{`${percentage}`}</Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
      )}

      <Box mt={4}>
        <Typography variant="h5" gutterBottom>
          Associated Articles
        </Typography>
        <List>
          {research.articles.map((article: any) => (
            <ListItem key={article.id}>
              <ListItemText
                primary={
                  <Link href={article.pdf_url || article.link} target="_blank" rel="noopener">
                    {article.title}
                  </Link>
                }
              />
            </ListItem>
          ))}
        </List>
      </Box>

      <Box mt={4}>
        <Typography variant="h5" gutterBottom>
          Related Articles
        </Typography>
        {relatedArticles.map((article: any) => (
            <ListItem key={article.id}>
              <ListItemText
                primary={
                  <Link href={article.pdf_url || article.link} target="_blank" rel="noopener">
                    {article.title}
                  </Link>
                }
              />
            </ListItem>
          ))}
      </Box>
    </div>
  );
};

export default ResearchPage;