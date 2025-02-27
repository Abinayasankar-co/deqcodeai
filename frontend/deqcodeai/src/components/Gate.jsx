import { useDrag } from 'react-dnd';

const Gate = ({ type, onDrop }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'GATE',
    item: { type },
    end: (item, monitor) => {
      const dropResult = monitor.getDropResult();
      if (item && dropResult) {
        onDrop(item.type, dropResult.qubit, dropResult.column);
      }
    },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));

  return (
    <div
      ref={drag}
      className={`w-10 h-10 bg-blue-500 text-white flex items-center justify-center rounded cursor-move ${isDragging ? 'opacity-50' : ''}`}
    >
      {type}
    </div>
  );
};

export default Gate;