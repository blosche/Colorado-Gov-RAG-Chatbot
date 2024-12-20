import React, { useState } from "react";
import {
  Modal,
  Box,
  Typography,
  TextField,
  Button,
  CircularProgress,
  IconButton,
  Avatar,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import ChatbotIcon from "../assets/ChatIcon.png"; 

import ChatMessage from "./ChatMessage";

interface ChatModalProps {
  open: boolean;
  handleClose: () => void;
  conversationId: string;
}

const ChatModal: React.FC<ChatModalProps> = ({
  open,
  handleClose: closeCallback,
  conversationId,
}) => {
  const [message, setMessage] = useState<string>("");
  const [chatHistory, setChatHistory] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleCloseWithDelete = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/end_conversation/${conversationId}`,
        { method: "DELETE" }
      );
      if (response.ok) {
        console.log("Conversation ended successfully.");
      } else {
        console.error("Error ending the conversation.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
    setIsLoading(false);
    closeCallback();
  };

  const handleSend = async () => {
    setIsLoading(true);
    const apiUrl = `http://localhost:8000/conversation/${conversationId}`;
    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: message }),
      });
      const data = await response.json();
      if (response.ok) {
        setChatHistory(data.response);
        console.log("Data fetched successfully:", data);
        console.log("Chat history:", chatHistory);
        setMessage("");
      } else {
        console.error("Error fetching data:", data);
      }
    } catch (error) {
      console.error("Error:", error);
    }
    setIsLoading(false);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Enter" && !isLoading) {
      handleSend();
    }
  };

  const modalStyle = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 600, 
    bgcolor: "background.paper",
    boxShadow: 24,
    p: 4,
    minHeight: 500,
    display: "flex",
    flexDirection: "column",
    borderRadius: "16px", 
  };

  const headerStyle = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    position: "relative",
    mb: 2,
  };

  const closeButtonStyle = {
    position: "absolute",
    top: 2,
    right: 2,
    transition: "transform 0.3s ease-in-out",
    "&:hover": {
      transform: "rotate(180deg)",
      backgroundColor: "rgba(255, 255, 255, 0.3)",
    },
  };

  return (
    <Modal
      open={open}
      onClose={handleCloseWithDelete}
      aria-labelledby="chat-modal"
      aria-describedby="chat-modal-for-sending-messages"
      BackdropProps={{
        onClick: (event) => event.stopPropagation(),
      }}
    >
      <Box sx={modalStyle}>
        <Box sx={headerStyle}>
          <Avatar src={ChatbotIcon} sx={{ width: 50, height: 50, mb: 1 }} />
          <Typography variant="h6" component="h2" style={{ color: "black" }}>
            Ask about our services or about unemployment benefits!
          </Typography>
          <IconButton onClick={handleCloseWithDelete} sx={closeButtonStyle}>
            <CloseIcon />
          </IconButton>
        </Box>
        <Box sx={{ maxHeight: 350, overflow: "auto", mb: 2, flexGrow: 1 }}>
          {chatHistory.map((msg, index) => (
            <ChatMessage
              key={index}
              isUser={msg.role === "human"}
              text={msg.content}
            />
          ))}
        </Box>
        <Box sx={{ mt: "auto" }}>
          {" "}
          {/* Input and Send button at the bottom */}
          <TextField
            label="Enter text..."
            fullWidth
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            variant="outlined"
            margin="normal"
            disabled={isLoading}
            autoComplete="off" 
          />
          {isLoading ? (
            <CircularProgress
              size={24}
              sx={{
                position: "absolute",
                top: "50%",
                left: "50%",
                marginTop: "-12px",
                marginLeft: "-12px",
              }}
            />
          ) : (
            <Button
              variant="contained"
              color="primary"
              onClick={handleSend}
              fullWidth
              style={{
                backgroundColor: "darkblue",
                color: "white",
                marginTop: 8,
              }}
            >
              Send Request
            </Button>
          )}
        </Box>
      </Box>
    </Modal>
  );
};

export default ChatModal;
