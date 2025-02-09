import { useState } from "react";

const QueryPage = () => {
  const [query, setQuery] = useState("");
  const [output, setOutput] = useState("No output");

  const handleSubmit = async () => {
    if (!query.trim()) return;
    const formdata = new FormData();
    formdata.append("query",query);
    try {
      const response = await fetch("/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();
      setOutput(data.response || "No response received");
    } catch (error) {
      setOutput("Error fetching response");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white p-6">
      <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Query Input Section */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold mb-4">Custom Query</h2>
          <textarea
            className="w-full p-3 bg-gray-900 text-white rounded-md border border-gray-600 focus:ring-2 focus:ring-gray-500"
            rows="4"
            placeholder="Type your query..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          ></textarea>
          <button
            className="mt-4 w-full bg-gray-700 hover:bg-gray-600 text-white py-2 rounded-md"
            onClick={handleSubmit}
          >
            Submit
          </button>
        </div>

        {/* Output Section */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold mb-4">Output</h2>
          <div className="p-3 bg-gray-900 text-white rounded-md border border-gray-600 min-h-[100px]">
            {output}
          </div>
        </div>
      </div>
    </div>
  );
};

export default QueryPage;
