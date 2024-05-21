import { css } from "@emotion/css";
import { Button, SnackbarContent } from "@mui/material";
import React from "react";

const snackbarContainerStyles = css`
  display: flex;
  position: fixed;
  bottom: 24px;
  width: 100%;
  justify-content: center;
`;

const Snackbar = ({ text, onActionLabel, onActionClicked }: {text: string; onActionLabel: string; onActionClicked?: () => void; }) => {

  return (
    <div className={snackbarContainerStyles}>
      <SnackbarContent
        message={text}
        action={(
          <Button size="small" onClick={onActionClicked}>
            {onActionLabel}
          </Button>
        )}
      />
    </div>
  );
}

export default Snackbar;