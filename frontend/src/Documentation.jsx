import React from 'react'

const Documentation = () => {
    return (
        <div className='documentation'>
            <div className='architecturalDecisions'>
                <p className='architectTitle'>Software Architecture</p>
                <p className="architectAnswer">Modular Monolith</p>
                <p className='architectWhy'>The system is designed as a modular monolith with clear domain boundaries, making it easy to evolve into microservices if needed. Not Mircoservices, since we don't have multiple teams, indpendant deployment, separate scaling needs and infra complexity</p>
                
            </div>

        </div>
    )
}

export default Documentation
