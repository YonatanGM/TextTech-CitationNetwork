// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyANcdEMuGkTxNQxSwc7Tkb6PGq8Ma1Zab8",
  authDomain: "texttech-citationnetwork.firebaseapp.com",
  projectId: "texttech-citationnetwork",
  storageBucket: "texttech-citationnetwork.appspot.com",
  messagingSenderId: "873332739696",
  appId: "1:873332739696:web:ead17c6b9797785e5feeb5"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// Initialize Realtime Database and get a reference to the service
const database = getDatabase(app);