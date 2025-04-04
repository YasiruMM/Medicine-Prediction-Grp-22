import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
const firebaseConfig = {
    apiKey: "AIzaSyCWnFq9tvolJ-DOd8jc1e5Qq53BGC5ZX3g",
    authDomain: "meditrack-72ddf.firebaseapp.com",
    projectId: "meditrack-72ddf",
    storageBucket: "meditrack-72ddf.firebasestorage.app",
    messagingSenderId: "1020641673174",
    appId: "1:1020641673174:web:42026d776a15d04683ee77"
  };
  const app = initializeApp(firebaseConfig);
  export const auth = getAuth(app);  