import Header from './components/Header'
import QuizForm from './pages/QuizForm'

export default function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-start p-4">
      <Header />
      <QuizForm />
    </div>
  )
}
