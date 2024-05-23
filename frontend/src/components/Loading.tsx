import React from "react";
import { css } from "@emotion/css";
import { CircularProgress } from "@mui/material";

const loadingContainerStyles = css`
  display: flex;
  position: absolute;
  top: 50%;
  left: 50%;
`;

const Loading = () => {
  return (
    <div className={loadingContainerStyles}>
        <CircularProgress />
    </div>
  )
};

export default Loading;