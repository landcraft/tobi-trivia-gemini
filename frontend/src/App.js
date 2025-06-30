// frontend/src/App.js - Your React application code
import React, { useState, useEffect, useRef } from 'react';
import { Sparkles, Brain, RefreshCw, ChevronDown, CheckCircle, Lightbulb, XCircle, ArrowRight } from 'lucide-react';

// Main App Component
const App = () => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [quizCompleted, setQuizCompleted] = useState(false);
  const [historyOfQuestions, setHistoryOfQuestions] = useState([]); // To prevent recent repeats (in-session only)

  // Topics for LLM to focus on
  const triviaTopics = "maths (addition, subtraction, multiplication, division, dates, times), science, space (solar system), literature (books like Dog Man, Pokémon, Diary of a Wimpy Kid)";

  // Function to fetch questions from the backend
  const fetchQuestions = async () => {
    setLoading(true);
    setErrorMessage('');
    setQuizCompleted(false);
    setCurrentQuestionIndex(0);
    setScore(0);
    setQuestions([]); // Clear previous questions immediately to show loading

    try {
      // Prompt for the LLM to generate trivia questions with multiple choices
      // This prompt will be sent to the backend, which will then call the LLM.
      const prompt = `Generate 10 engaging, humorous, and moderately difficult multiple-choice trivia questions suitable for 7-10 year olds.
      Each question should have a clear question and exactly four distinct options (A, B, C, D), with one correct answer.
      Focus on topics: ${triviaTopics}.
      Questions should be relevant to UK, Europe, or US audiences.
      Ensure no direct repeats from the following recent questions: ${historyOfQuestions.slice(-20).map(q => q.question).join(', ')}.
      Format the output as a JSON array of objects, where each object has 'question', 'options' (an array of objects with 'key' and 'text'), and 'correctAnswerKey' (the key of the correct option, e.g., "A").`;

      // Call the backend endpoint to generate trivia
      // CORRECTED: Use the service name 'tobi-trivia-backend' for inter-container communication
      const backendUrl = 'http://tobi-trivia-backend:5000/generate_trivia';
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt }) // Send the prompt to the backend
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status} ${response.statusText}`);
      }

      const parsedQuestions = await response.json();

      // Simple in-session repeat prevention for generated questions
      const newQuestions = parsedQuestions.filter(q =>
        !historyOfQuestions.some(h => h.question.toLowerCase() === q.question.toLowerCase())
      );

      if (newQuestions.length < 10) {
          console.warn(`Generated ${newQuestions.length} unique questions. Attempting to get more if possible.`);
          // In a real scenario, you'd refine the LLM call or backend logic to ensure 10 unique questions.
      }

      setQuestions(newQuestions.slice(0, 10)); // Take up to 10 questions
      setCurrentQuestionIndex(0); // Start from the first question
      setScore(0); // Reset score
      setQuizCompleted(false); // Reset quiz completion state

      // Update history, keeping it to a reasonable size (e.g., last 50 questions)
      setHistoryOfQuestions(prev => [...prev, ...newQuestions].slice(-50));

    } catch (error) {
      console.error("Error fetching questions:", error);
      setErrorMessage(`Failed to load questions. Please try again. (${error.message})`);
      setQuestions([]);
    } finally {
      setLoading(false);
    }
  };

  // Handle answer selection (updates score only)
  const handleAnswerSelected = (isCorrect) => {
    if (isCorrect) {
      setScore(prevScore => prevScore + 1);
    }
  };

  // Handle moving to the next question
  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prevIndex => prevIndex + 1);
    } else {
      setQuizCompleted(true);
    }
  };

  // Fetch questions on initial load
  useEffect(() => {
    fetchQuestions();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500 flex flex-col items-center p-4 font-inter">
      <h1 className="text-5xl md:text-6xl font-bold text-white mb-8 drop-shadow-lg text-center leading-tight">
        <Sparkles className="inline-block w-12 h-12 md:w-16 md:h-16 mr-2 text-yellow-300" />
        Tobi's Daily Trivia!
        <Sparkles className="inline-block w-12 h-12 md:w-16 md:h-16 ml-2 text-yellow-300" />
      </h1>

      <div className="w-full max-w-4xl bg-white rounded-3xl shadow-xl p-6 md:p-8 mb-8 flex flex-col items-center">
        <div className="flex flex-col md:flex-row justify-between items-center w-full mb-6">
          <p className="text-gray-700 text-lg md:text-xl font-semibold mb-4 md:mb-0">
            Brain-teasing questions for smart kids!
          </p>
          <button
            onClick={fetchQuestions}
            disabled={loading}
            className="flex items-center bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-full shadow-lg transition duration-300 ease-in-out transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <RefreshCw className="animate-spin mr-2" />
                Loading...
              </>
            ) : (
              <>
                <RefreshCw className="mr-2" />
                New Questions
              </>
            )}
          </button>
        </div>

        {errorMessage && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-xl relative mb-6 w-full" role="alert">
            <strong className="font-bold">Oops!</strong>
            <span className="block sm:inline ml-2">{errorMessage}</span>
          </div>
        )}

        {loading && (
          <div className="text-center text-blue-500 text-xl py-10">
            <RefreshCw className="animate-spin inline-block mr-2" size={32} />
            Getting new trivia for Tobi...
          </div>
        )}

        {!loading && questions.length === 0 && !errorMessage && (
          <div className="text-center text-gray-500 text-xl py-10">
            No questions loaded yet. Click 'New Questions' to start!
          </div>
        )}

        {!loading && questions.length > 0 && !quizCompleted && (
          <QuizQuestionCard
            questionData={questions[currentQuestionIndex]}
            questionNumber={currentQuestionIndex + 1}
            totalQuestions={questions.length}
            onAnswerSelected={handleAnswerSelected}
            onNextQuestion={handleNextQuestion}
          />
        )}

        {!loading && quizCompleted && questions.length > 0 && (
          <QuizResults
            score={score}
            totalQuestions={questions.length}
            onPlayAgain={fetchQuestions}
          />
        )}
      </div>

      <p className="text-white text-sm opacity-80 mt-8 text-center">
        Powered by fun and curiosity!
      </p>
    </div>
  );
};

// Quiz Question Card Component
const QuizQuestionCard = ({ questionData, questionNumber, totalQuestions, onAnswerSelected, onNextQuestion }) => {
  const [selectedAnswerKey, setSelectedAnswerKey] = useState(null);
  const [feedback, setFeedback] = useState(null); // 'correct', 'incorrect', or null

  useEffect(() => {
    // Reset state when questionData changes (i.e., new question loaded)
    setSelectedAnswerKey(null);
    setFeedback(null);
  }, [questionData]);

  const handleOptionClick = (optionKey) => {
    if (selectedAnswerKey !== null) return; // Prevent multiple selections

    setSelectedAnswerKey(optionKey);
    const isCorrect = optionKey === questionData.correctAnswerKey;
    setFeedback(isCorrect ? 'correct' : 'incorrect');
    onAnswerSelected(isCorrect); // Notify parent component about answer correctness
  };

  const getButtonClass = (optionKey) => {
    let classes = "w-full text-left py-3 px-4 rounded-xl text-lg font-medium transition duration-200 ease-in-out transform hover:scale-105 ";
    if (selectedAnswerKey === null) {
      // No answer selected yet
      classes += "bg-purple-100 hover:bg-purple-200 text-purple-800 shadow";
    } else {
      // An answer has been selected
      if (optionKey === questionData.correctAnswerKey) {
        // Correct answer (always green if it's the correct one)
        classes += "bg-green-200 text-green-800 shadow-md";
      } else if (optionKey === selectedAnswerKey) {
        // Incorrect answer that was selected (red)
        classes += "bg-red-200 text-red-800 shadow-md";
      } else {
        // Other incorrect answers (grayed out)
        classes += "bg-gray-100 text-gray-500 opacity-70 cursor-not-allowed";
      }
    }
    return classes;
  };

  return (
    <div className="bg-gradient-to-r from-blue-100 to-indigo-100 p-6 rounded-3xl shadow-xl border border-blue-200 w-full">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-blue-700 text-2xl md:text-3xl font-bold">
          Question {questionNumber} / {totalQuestions}
        </h2>
        {feedback === 'correct' && (
          <CheckCircle className="text-green-500 animate-bounce-in" size={40} />
        )}
        {feedback === 'incorrect' && (
          <XCircle className="text-red-500 animate-shake" size={40} />
        )}
      </div>

      <div className="flex items-start mb-6">
        <Brain className="text-blue-500 mr-4 mt-1 flex-shrink-0" size={32} />
        <p className="text-gray-800 text-xl md:text-2xl font-semibold leading-relaxed">
          {questionData.question}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {questionData.options.map((option) => (
          <button
            key={option.key}
            onClick={() => handleOptionClick(option.key)}
            disabled={selectedAnswerKey !== null} // Disable buttons once an answer is selected
            className={getButtonClass(option.key)}
          >
            <span className="font-bold mr-2">{option.key}:</span> {option.text}
          </button>
        ))}
      </div>

      {selectedAnswerKey !== null && ( // Show feedback and next button only after selection
        <>
          <div className={`mt-6 p-4 rounded-xl shadow-inner flex items-center
            ${feedback === 'correct' ? 'bg-green-100 border border-green-300 text-green-700' : 'bg-red-100 border border-red-300 text-red-700'}`}>
            <Lightbulb className={`mr-3 ${feedback === 'correct' ? 'text-green-500' : 'text-red-500'}`} size={24} />
            <p className="font-bold text-lg">
              {feedback === 'correct' ? "That's correct! 🎉" : "Oops! Not quite. Better luck next time!"}
            </p>
          </div>

          <div className="mt-6 text-center">
            <button
              onClick={onNextQuestion}
              className="inline-flex items-center bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-full shadow-lg transition duration-300 ease-in-out transform hover:scale-105"
            >
              Next Question <ArrowRight className="ml-2" />
            </button>
          </div>
        </>
      )}
    </div>
  );
};

// Quiz Results Component
const QuizResults = ({ score, totalQuestions, onPlayAgain }) => {
  const percentage = (score / totalQuestions) * 100;
  let message = "";
  let icon = null;

  if (percentage === 100) {
    message = "Amazing! You're a trivia superstar! 🌟";
    icon = <Sparkles className="text-yellow-400 mr-2" size={48} />;
  } else if (percentage >= 70) {
    message = "Great job! You've got a super brain! 💪";
    icon = <CheckCircle className="text-green-500 mr-2" size={48} />;
  } else if (percentage >= 40) {
    message = "Good effort! Keep practicing, you'll get even better! 👍";
    icon = <Lightbulb className="text-blue-500 mr-2" size={48} />;
  } else {
    message = "You tried your best! Every day is a chance to learn something new! 🌈";
    icon = <Brain className="text-purple-500 mr-2" size={48} />;
  }

  return (
    <div className="bg-gradient-to-br from-green-200 to-blue-200 p-8 rounded-3xl shadow-xl border-2 border-green-300 text-center w-full max-w-md animate-fade-in">
      <h2 className="text-4xl font-bold text-gray-800 mb-6">Quiz Completed!</h2>
      <div className="flex items-center justify-center mb-6">
        {icon}
        <p className="text-6xl font-extrabold text-blue-700">{score}/{totalQuestions}</p>
      </div>
      <p className="text-2xl font-semibold text-gray-700 mb-8">{message}</p>
      <button
        onClick={onPlayAgain}
        className="flex items-center justify-center bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-8 rounded-full shadow-lg transition duration-300 ease-in-out transform hover:scale-105"
      >
        <RefreshCw className="mr-3" />
        Play Again!
      </button>
    </div>
  );
};

export default App;
