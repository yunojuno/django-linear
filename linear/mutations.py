from linear.queries import run_query


def create_issue(team_id: str, title: str, description: str, label_id: str) -> None:
    """Create a new issue in Linear."""
    mutation = """
      mutation (
          $title: String!
          $description: String!
          $teamId: String!
          $labelId: String
      ) {
      issueCreate(
          input: {
          title: $title
          description: $description
          teamId: $teamId
          labelIds: [$labelId]
          }
      ) {
          success
          issue {
          id
          title
          }
        }
      }
    """
    run_query(
        mutation,
        teamId=team_id,
        title=title,
        description=description,
        labelId=label_id,
    )
