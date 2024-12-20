import { useState } from "react";
import ChatModal from "./components/ChatModal";
import IconButton from "@mui/material/IconButton";
import Avatar from "@mui/material/Avatar";
import ChatbotIcon from "./assets/ChatMain.png"; 

import "./App.css";

function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [conversationId, setConversationId] = useState("");

  const handleOpenModal = async () => {
    try {
      const response = await fetch("http://localhost:8000/start_conversation", {
        method: "POST",
      });
      const data = await response.json();
      if (response.ok) {
        setConversationId(data.conversation_id);
        console.log("Received conversation ID:", data.conversation_id);
        setIsModalOpen(true);
      } else {
        console.error("Error fetching conversation ID:", data);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="App">
      <div className="background"></div>
      <div className="intro-container">
        {/* <h1 style={{ color: "black" }}>Welcome to colorado.gov</h1> */}
        {/* <p style={{ color: "black" }}> For any inquires into our services please search the list or use our virtual assistant in the bottom right.</p> */}
      </div>
      <IconButton
        onClick={handleOpenModal}
        style={{
          position: "fixed",
          bottom: 20,
          right: 20,
          backgroundColor: "#fff",
          borderRadius: "50%",
          width: "110px",
          height: "110px",
          padding: 15,
        }}
      >
        <Avatar
          src={ChatbotIcon}
          alt="Open Chat"
          style={{
            width: "110px",
            height: "110px",
          }}
        />
      </IconButton>
      {isModalOpen && (
        <ChatModal
          open={isModalOpen}
          handleClose={handleCloseModal}
          conversationId={conversationId}
        />
      )}
    </div>
  );
}

export default App;
