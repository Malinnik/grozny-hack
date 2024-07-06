const DownloadSubmission = ({id, filename, ready}: {id: number, filename: string, ready: boolean}) => {

    const handleClick = () => {

        const getServerSideProps = (async () => {
            const res = await fetch(`api/v1/submissions/csv?id=${id}`) 
            const repo = await res.json()
            return { props: { repo } } 
          })
        
        getServerSideProps()

        fetch(`api/v1/submissions/csv?id=${id}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/octet-stream',
            },
          })
          .then((response) => response.blob())
          .then((blob) => {
            // Create blob link to download
            const url = window.URL.createObjectURL(
              new Blob([blob]),
            );
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute(
              'download',
              `${filename}`,
            );
            // Append to html link element page
            document.body.appendChild(link);
            // Start download
            link.click();
            // Clean up and remove the link
            link.parentNode?.removeChild(link);
          });
    }
    
    return (
      // className="rounded-lg text-blue-500 hover:text-white hover:bg-blue-500 border border-blue-500"
        <button className={ready ? 
          "rounded-lg text-blue-500 hover:text-white hover:bg-blue-500 border border-blue-500" : 
          " bg-white  text-gray-400 font-semibold border rounded"} onClick={handleClick}>
            <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-8"> 
              <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" /> 
            </svg>
        </button>
    )
}

export default DownloadSubmission;