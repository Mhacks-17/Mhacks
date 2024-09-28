import React from "react";
import { View, Text, StyleSheet, TouchableOpacity, Image } from "react-native";

interface MainPageProps {
  onAskQuestion: () => void;
  onUseVoice: () => void;
  onAddPicture: () => void;
}

const MainPage: React.FC<MainPageProps> = ({
  onAskQuestion,
  onUseVoice,
  onAddPicture,
}) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>How Can We Assist You Today?</Text>
      <Text style={styles.tipText}>Choose an option to get started!</Text>
      <View style={styles.optionContainer}>
        <TouchableOpacity style={styles.optionButton} onPress={onAskQuestion}>
          <Image
            source={require("./questions.png")}
            style={styles.optionIcon}
          />
          <Text style={styles.optionText}>Ask a Question via text</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.optionButton} onPress={onUseVoice}>
          <Image source={require("./mic.png")} style={styles.optionIcon} />
          <Text style={styles.optionText}>Ask a Question via voice</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.optionButton} onPress={onAddPicture}>
          <Image source={require("./pic.png")} style={styles.optionIcon} />
          <Text style={styles.optionText}>Add Picture </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#e0f7fa",
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#006064",
    marginBottom: 30,
    textAlign: "center",
  },
  optionContainer: {
    width: "100%",
    justifyContent: "center",
    alignItems: "center",
  },
  tipText: {
    fontSize: 16,
    color: "#004d40",
    marginBottom: 20,
    textAlign: "center",
  },
  optionButton: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#00796b",
    paddingVertical: 15,
    paddingHorizontal: 25,
    borderRadius: 30,
    marginVertical: 10,
    width: "80%",
    justifyContent: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 5 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
  },
  optionText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "bold",
    marginLeft: 10,
  },
  optionIcon: {
    width: 30,
    height: 30,
    tintColor: "#fff",
  },
});

export default MainPage;
