const Navbar = ({ username }) => (
    <nav className="bg-gray-900 text-white p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold">Quantum Circuits</h1>
      <span className="text-orange-400">{username}</span>
    </nav>
  );

export default Navbar;