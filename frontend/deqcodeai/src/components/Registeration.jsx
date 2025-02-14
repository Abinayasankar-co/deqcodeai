import { useState } from 'react';
import { ChevronRight, Eye, EyeOff, User, Mail, Book, Target, GraduationCap, Heart, Search, FileText, Lock } from 'lucide-react';
import { useAuth } from '../AuthContext';
import { useNavigate } from 'react-router-dom';
import React from 'react';

const Register = () => {
  const {setIsAuthenticated, setUsername} = useAuth();
  const [formData, setFormData] = useState({
    userId: '',
    name: '',
    email: '',
    password: '',
    competency: '',
    purpose: '',
    education: '',
    preference: '',
    foundBy: '',
    review: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const nextStep = () => {
    setCurrentStep(prev => Math.min(prev + 1, 3));
  };

  const prevStep = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(formData);
    try{
      const register = await fetch('/api/register',{
           method:"POST",
           headers:{
            'ContentType' : 'application/json'
           },
           body: JSON.stringify(formData)

      })
      if(register.ok){
        const data = register.json();
        localStorage.setItem("session_token",data.session_key);
        localStorage.setItem('username', formData.username);
        setIsAuthenticated(true);
        setUsername(formData.username);
        navigate('/design');
      }
      else{
        console.log(e);
        navigate('/registration_error');
      }
    }catch(e){
      console.log(e);
      navigate('/registration_error');
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
        <div className="p-8">
          <div className='text-3xl text-center text-white mb-2 font-sans font-bold'>Deqcode Welocomes You!</div>
          <h2 className="text-3xl font-bold text-white mb-2 font-sans">Create Account</h2>
          <div className="h-1 w-20 bg-purple-500 mb-6"></div>
          
          <div className="mb-8 flex justify-between">
            {[1, 2, 3].map((step) => (
              <div key={step} className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  currentStep >= step ? 'bg-purple-500' : 'bg-gray-700'
                } text-white font-bold`}>
                  {step}
                </div>
                {step < 3 && (
                  <div className={`w-24 h-1 mx-2 ${
                    currentStep > step ? 'bg-purple-500' : 'bg-gray-700'
                  }`}></div>
                )}
              </div>
            ))}
          </div>

          <form onSubmit={handleSubmit}>
            {currentStep === 1 && (
              <div className="space-y-6">
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    name="userId"
                    placeholder="User ID"
                    className="w-full bg-gray-700 text-white pl-12 pr-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
                    value={formData.userId}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="email"
                    name="email"
                    placeholder="Email Address"
                    className="w-full bg-gray-700 text-white pl-12 pr-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
                    value={formData.email}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    name="password"
                    placeholder="Password"
                    className="w-full bg-gray-700 text-white pl-12 pr-12 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
                    value={formData.password}
                    onChange={handleChange}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white"
                  >
                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                  </button>
                </div>
              </div>
            )}

            {currentStep === 2 && (
              <div className="space-y-6">
                <div className="relative">
                  <Book className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    name="competency"
                    placeholder="Your Competency"
                    className="w-full bg-gray-700 text-white pl-12 pr-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
                    value={formData.competency}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="relative">
                  <Target className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    name="purpose"
                    placeholder="Purpose"
                    className="w-full bg-gray-700 text-white pl-12 pr-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
                    value={formData.purpose}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="relative">
                  <GraduationCap className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    name="education"
                    placeholder="Education"
                    className="w-full bg-gray-700 text-white pl-12 pr-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
                    value={formData.education}
                    required
                    onChange={handleChange}
                  />
                </div>
              </div>
            )}

            {currentStep === 3 && (
              <div className="space-y-6">
                <div className="relative">
                  <Heart className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    name="preference"
                    placeholder="Your Preference"
                    className="w-full bg-gray-700 text-white pl-12 pr-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
                    value={formData.preference}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    name="foundBy"
                    placeholder="How did you find us?"
                    className="w-full bg-gray-700 text-white pl-12 pr-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
                    value={formData.foundBy}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="relative">
                  <FileText className="absolute left-3 top-6 text-gray-400" size={20} />
                  <textarea
                    name="review"
                    placeholder="Your Review"
                    className="w-full bg-gray-700 text-white pl-12 pr-4 py-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all min-h-[100px]"
                    value={formData.review}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
            )}

            <div className="mt-8 flex justify-between">
              {currentStep > 1 && (
                <button
                  type="button"
                  onClick={prevStep}
                  className="px-6 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-all"
                >
                  Previous
                </button>
              )}
              {currentStep < 3 ? (
                <button
                  type="button"
                  onClick={nextStep}
                  className="px-6 py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-all ml-auto flex items-center"
                >
                  Next
                  <ChevronRight className="ml-2" size={20} />
                </button>
              ) : (
                <button
                  type="submit"
                  className="px-6 py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-all ml-auto"
                >
                  Create Account
                </button>
              )}
            </div>
          </form>

          <div className="mt-6 text-center text-gray-400">
            Already have an account?{' '}
            <a href="/login" className="text-purple-500 hover:text-purple-400 transition-all">
              Sign in
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;