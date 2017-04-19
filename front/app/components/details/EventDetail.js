import React from 'react';
require('../../../public/sass/EventDetail.scss');

/* Redux */
import { connect } from 'react-redux';
import * as actionCreators from '../redux/actionCreators';

/**
 * Presents event information / allows the user
 * to reject or accept events accordingly
 */
class EventDetail extends React.Component {

  /**
   * Constructor
   */
  constructor (props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  /**
   * Handle click
   */
  handleClick (e) {
    // Relevant / irrelevant listings
    let relevant = this.props.relevant;
    let irrelevant = this.props.irrelevant;

    // Remove this event from relevant + add it to irrelevant
    relevant.splice(relevant.indexOf(this.props.data.id), 1);
    irrelevant.push(this.props.data.id);

    // Dispatch this event b/c relevance changed
    this.props.dispatch(
      actionCreators.didChangeRelevance(this.props.currentQuery, relevant, irrelevant)
    );
  }

  /**
   * Render
   */
  render () {
    return (
      <div className='event-detail-container'>
        <div className='event-detail-img'>
          <img src={this.props.data.profile_picture} />
        </div>
        {/* Title */}
        <div className='event-detail-title'>
          {this.props.data.name}
        </div>
        {/* Venue */}
        <div className='event-detail-venue'>
          <p>{this.props.data.place.name}</p>
        </div>
        {/* Date */}
        <div className='event-detail-date'>
          <p>{this.props.data.date}</p>
        </div>
        {/* Description */}
        <div className='event-detail-description'>
          {this.props.data.description}
        </div>
        <button
          className='event-detail-dismiss fa fa-times'
          onClick={this.handleClick} />
      </div>
    );
  }
}

/** Map the redux state to this component's props */
const mapStateToProps = (state) => {
  return {
    currentQuery: state._search.query,
    relevant: state._search.results.events.relevant,
    irrelevant: state._search.results.events.irrelevant
  };
};

export default connect(mapStateToProps)(EventDetail);
