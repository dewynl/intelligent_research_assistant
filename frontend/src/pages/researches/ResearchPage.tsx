import React, { useEffect, useState } from 'react';
import { format } from 'date-fns';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import axiosInstance from '../../axios';
import Loading from '../../components/Loading';

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
    <div className="research-page">
      <h1>Research Details</h1>
      <div className="research-info">
        <p>
          <strong>Research ID:</strong> {research?.id}
        </p>
        <p>
          <strong>Category:</strong> {research?.research_category}
        </p>
        <p>
          <strong>Keywords:</strong> {research?.keywords.join(', ')}
        </p>
        <p>
          <strong>Preprocess Status:</strong> {research?.research_preprocess_status}
        </p>
        <p>
          <strong>Summary Generation Status:</strong> {research?.ummary_generation_status}
        </p>
      </div>

      <div className="research-summary">
        <h2>Summary</h2>
        <p>{research?.summary}</p>
      </div>

      <div className="research-articles">
        <h2>Related Articles</h2>
        {research?.articles.map((article: any) => (
          <div key={article.id} className="article-card">
            <h3>{article.title}</h3>
            <p>
              <strong>Abstract:</strong> {article.abstract}
            </p>
            <p>
              <strong>Link:</strong>{' '}
              <a href={article.link} target="_blank" rel="noopener noreferrer">
                {article.link}
              </a>
            </p>
            <p>
              <strong>DOI:</strong> {article.doi}
            </p>
            <p>
              <strong>PDF URL:</strong>{' '}
              <a href={article.pdf_url} target="_blank" rel="noopener noreferrer">
                {article.pdf_url}
              </a>
            </p>
            <p>
              <strong>Source:</strong> {article.source}
            </p>
            <p>
              <strong>Source ID:</strong> {article.source_id}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResearchPage;