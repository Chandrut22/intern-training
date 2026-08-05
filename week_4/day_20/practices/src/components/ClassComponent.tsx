import React from "react";

interface Props {
  name: string;
}

class ClassComponent extends React.Component<Props> {
  render() {
    return (
      <h1>Hello {this.props.name}</h1>
    );
  }
}

export default ClassComponent;

