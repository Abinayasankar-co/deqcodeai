import React, { useState } from 'react';
import { FaEye, FaEyeSlash , FaCalendarAlt} from 'react-icons/fa';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { useNavigate } from 'react-router-dom';

function Registration() {
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();
  const [date, setDate] = useState('');
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    competency: '',
    purpose: '',
    education: '',
    foundby: '',
    review: '',
    notesbyuser: '',
    preference: '',
    dateofjoin: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Submitted Data:', formData);
    try {
      localStorage.setItem('username', formData.username);
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        alert('Registration successful!');
      } else {
        alert('Error registering user');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred.');
      navigate('/error_portal')
    }
  };

  return (
    <div className="bg-gray-900 text-white min-h-screen flex items-center justify-center">
      <div className="max-w-md w-full bg-gray-800 p-6 rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold text-gray-100 text-center mb-6">Register</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300">User Name</label>
            <input
              type="text"
              name="user_name"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter your user name"
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300">Competency</label>
            <select
              name="competency"
              value={formData.competency}
              onChange={handleChange}
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
            >
              <option value="" disabled>Select your competency</option>
              <option value="Researcher">Researcher</option>
              <option value="Scholar">Scholar</option>
              <option value="Student">Student</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300">Purpose</label>
            <select
              name="purpose"
              value={formData.purpose}
              onChange={handleChange}
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
            >
              <option value="" disabled>Select the purpose</option>
              <option value="Research">Research</option>
              <option value="Work">Work</option>
              <option value="Company Preferal">Company Preferal</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300">Education</label>
            <select
              name="education"
              value={formData.education}
              onChange={handleChange}
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
            >
              <option value="" disabled>Select your education level</option>
              <option value="School">School</option>
              <option value="College">College</option>
              <option value="Work">Work</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300">Preference:</label>
            <input
              type="text"
              name="preference"
              value={formData.preference}
              onChange={handleChange}
              placeholder="Enter your preference"
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300">Found By:</label>
            <select
              name="foundby"
              value={formData.foundby}
              onChange={handleChange}
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
            >
              <option value="" disabled>Select how you found us</option>
              <option value="College">College</option>
              <option value="Link">Link</option>
              <option value="Suggested">Suggested</option>
              <option value="Friends">Friends</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300">Review:</label>
            <textarea
              name="review"
              value={formData.review}
              onChange={handleChange}
              placeholder="Enter your review"
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
            />
          </div>
          <div>
           <label className="block text-sm font-medium text-gray-300">Password:</label>
             <div className="relative">
               <input
                    type={showPassword ? "text" : "password"}
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Enter your password"
                    className="w-full p-2 mt-1 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
                    required
                />
                <span
                   onClick={() => setShowPassword(!showPassword)}
                   className="absolute inset-y-0 right-3 flex items-center text-gray-400 cursor-pointer"
                >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
                </span>
             </div>
           </div>
          <div>
            <label className="block text-sm font-medium text-gray-300">Notes By User:</label>
            <textarea
              name="notesby_user"
              value={formData.notesbyuser}
              onChange={handleChange}
              placeholder="Enter your notes"
              className="w-full p-2 mt-1 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300">Date</label>
            <div className='relative flex items-centre'>
              <DatePicker
               selected={date ? new Date(date) : null}
               onChange={handleChange}
               dateFormat="yyyy-MM-dd"
               //className="absolute right-3 text-gray-400 hover:text-cyan-500 transition-colors duration-200"
               customInput={<FaCalendarAlt size={24}/>}
               className="w-96 p-2 mt-1 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
               placeholderText="Select a date"
              />
            </div>
          </div>
          <button
            type="submit"
            className="w-full py-2 mt-4 bg-cyan-500 text-orange font-bold rounded-md hover:bg-cyan-600 transition"
          >
            Register
          </button>
        </form>
      </div>
    </div>
  );
}

export default Registration;
