import ironmangif from '../assets/ironman.gif';

const IronManGif = () => {
  return (
    <div>    
      <div className="ironmancontainer" style={
        {
          position:'fixed',
          right:'10px',
          bottom:'10px'
        }
      }>
        <img height='200px' src={ironmangif} alt="Ironman" />
      </div>
    </div>
  )
}

export default IronManGif
