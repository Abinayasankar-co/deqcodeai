import React, { useState } from 'react';
import '../styles/registration_page.css';

function Registration() {
  const [formData, setFormData] = useState({
    user_name: '',
    password: '',
    competency: '',
    purpose: '',
    education: '',
    pack: '',
    preference: '',
    foundby: '',
    circuit_count: '',
    review: '',
    notesby_user: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Submitted Data:', formData);
    try {
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
    }
  };

  return (
    <div className="registration-container">
      <h1>Register</h1>
      <form onSubmit={handleSubmit}>
        <label>
          User Name:
          <input
            type="text"
            name="user_name"
            value={formData.user_name}
            onChange={handleChange}
            placeholder="Enter your user name"
            required
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
            required
          />
        </label>
        <label>
          Competency:
          <input
            type="text"
            name="competency"
            value={formData.competency}
            onChange={handleChange}
            placeholder="Enter your competency"
          />
        </label>
        <label>
          Purpose:
          <input
            type="text"
            name="purpose"
            value={formData.purpose}
            onChange={handleChange}
            placeholder="Enter the purpose"
          />
        </label>
        <label>
          Education:
          <input
            type="text"
            name="education"
            value={formData.education}
            onChange={handleChange}
            placeholder="Enter your education"
          />
        </label>
        <label>
          Pack:
          <input
            type="text"
            name="pack"
            value={formData.pack}
            onChange={handleChange}
            placeholder="Enter pack details"
          />
        </label>
        <label>
          Preference:
          <input
            type="text"
            name="preference"
            value={formData.preference}
            onChange={handleChange}
            placeholder="Enter your preference"
          />
        </label>
        <label>
          Found By:
          <input
            type="text"
            name="foundby"
            value={formData.foundby}
            onChange={handleChange}
            placeholder="Enter how you found us"
          />
        </label>
        <label>
          Circuit Count:
          <input
            type="number"
            name="circuit_count"
            value={formData.circuit_count}
            onChange={handleChange}
            placeholder="Enter the circuit count"
          />
        </label>
        <label>
          Review:
          <textarea
            name="review"
            value={formData.review}
            onChange={handleChange}
            placeholder="Enter your review"
          />
        </label>
        <label>
          Notes By User:
          <textarea
            name="notesby_user"
            value={formData.notesby_user}
            onChange={handleChange}
            placeholder="Enter your notes"
          />
        </label>
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Registration;
