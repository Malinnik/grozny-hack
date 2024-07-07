const Dot = ({status}) => {

    if (status === 'process') {
        return (
            <div className="bg-orange-500 rounded-full w-5 h-5"></div>
        )
    }
    if  (status === 'exited')  {
        return (
            <div className="bg-red-500 rounded-full w-5 h-5"></div>
        )
    }
    if (status === 'ready')   {
        return (
            <div className="bg-green-500 rounded-full w-5 h-5"></div>
        )
    }
}

export default Dot;