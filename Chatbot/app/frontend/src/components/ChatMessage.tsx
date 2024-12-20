import React from "react";
import ChatbotIcon from "../assets/ChatIcon.png";
import userImage from "../assets/user.png";

interface ChatMessageProps {
  isUser: boolean;
  text: string;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ isUser, text }) => {
  const chatStyle: React.CSSProperties = {
    display: "flex",
    flexDirection: "row", 
    justifyContent: isUser ? "flex-end" : "flex-start",
    alignItems: "center", 
    marginBottom: "10px",
  };

  const imageStyle: React.CSSProperties = {
    borderRadius: "50%",
    width: "50px",
    height: "50px",
    objectFit: "cover",
    margin: "0 10px",
  };

  const textStyle: React.CSSProperties = {
    maxWidth: "70%",
    padding: "10px",
    borderRadius: "15px",
    backgroundColor: isUser ? "darkblue" : "grey",
    color: "white",
    whiteSpace: "pre-wrap", // Preserves new lines
    wordWrap: "break-word",
  };

  // Function to format the text
  const formatText = (inputText: string) => {
    const boldText = inputText.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    const linkText = boldText.replace(
      /\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/g,
      '<a href="$2" style="color: lightblue;" target="_blank">$1</a>'
    );
    return { __html: linkText };
  };

  return (
    <div style={chatStyle}>
      {!isUser && <img src={ChatbotIcon} alt="AI" style={imageStyle} />}
      <div style={textStyle} dangerouslySetInnerHTML={formatText(text)} />
      {isUser && <img src={userImage} alt="User" style={imageStyle} />}
    </div>
  );
};

export default ChatMessage;
