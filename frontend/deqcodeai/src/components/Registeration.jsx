import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Form, Button } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';

const Register = () => {
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
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handlePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(formData);

    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.token) {
          localStorage.setItem('token', data.token);
        }
        navigate("/home");
      } else {
        console.error('Signup failed:', response.statusText);
        navigate("/Failedlogin");
      }
    } catch (error) {
      console.error('Error:', error);
      navigate("/Failedlogin");
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center vh-100">
      <Form onSubmit={handleSubmit} className="p-4 bg-dark text-white rounded w-50">
        <h2 className="text-center">Register</h2>
        <div className="d-flex justify-content-between border-bottom pb-3">
          <div className="w-50 pr-2">
            <Form.Group>
              <Form.Label>User ID</Form.Label>
              <Form.Control type="text" name="userId" value={formData.userId} onChange={handleChange} required />
            </Form.Group>
            <Form.Group>
              <Form.Label>Name</Form.Label>
              <Form.Control type="text" name="name" value={formData.name} onChange={handleChange} required />
            </Form.Group>
            <Form.Group>
              <Form.Label>Competency</Form.Label>
              <Form.Control type="text" name="competency" value={formData.competency} onChange={handleChange} required />
            </Form.Group>
            <Form.Group>
              <Form.Label>Purpose</Form.Label>
              <Form.Control type="text" name="purpose" value={formData.purpose} onChange={handleChange} required />
            </Form.Group>
          </div>
          <div className="w-50 pl-2">
            <Form.Group>
              <Form.Label>Email</Form.Label>
              <Form.Control type="email" name="email" value={formData.email} onChange={handleChange} required />
            </Form.Group>
            <Form.Group>
              <Form.Label>Education</Form.Label>
              <Form.Control type="text" name="education" value={formData.education} onChange={handleChange} required />
            </Form.Group>
            <Form.Group>
              <Form.Label>Preference</Form.Label>
              <Form.Control type="text" name="preference" value={formData.preference} onChange={handleChange} required />
            </Form.Group>
            <Form.Group>
              <Form.Label>Found By</Form.Label>
              <Form.Control type="text" name="foundBy" value={formData.foundBy} onChange={handleChange} required />
            </Form.Group>
          </div>
        </div>
        <Form.Group className="mt-3">
          <Form.Label>Review</Form.Label>
          <Form.Control as="textarea" name="review" value={formData.review} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mt-3 position-relative">
          <Form.Label>Password</Form.Label>
          <Form.Control type={showPassword ? 'text' : 'password'} name="password" value={formData.password} onChange={handleChange} required />
          <faEye className="position-absolute" onClick={handlePasswordVisibility} />
        </Form.Group>
        <Button variant="light" type="submit" className="mt-3 w-100">Submit</Button>
        <div className='text-center py-2'>Already Have an Account?</div>
        <Button variant="light" href='/login' type='button' className="mt-1 w-100">Login</Button>
      </Form>
    </Container>
  );
};

export default Register;
