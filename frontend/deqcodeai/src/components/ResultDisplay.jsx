const ResultDisplay = ({ url, content }) => (
    <div className="p-4 bg-gray-700 text-white rounded-lg">
      <p>{content}</p>
      {url && (
        <a href={url} className="text-orange-400 underline">
          View More
        </a>
      )}
    </div>
  );
  
  export default ResultDisplay;