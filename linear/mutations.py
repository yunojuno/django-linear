from linear.queries import run_query


def create_issue(
    team_id: str,
    title: str,
    description: str,
    label_id: str,
    subscriber_id: str,
) -> None:
    """Create a new issue in Linear."""
    # need to pass empty JS array, not [""]
    subscriber_ids = [subscriber_id] if subscriber_id else []
    mutation = """
        mutation (
        $title: String!
        $description: String!
        $teamId: String!
        $labelId: String!
        $subscriberIds: [String!]
        ) {
        issueCreate(
            input: {
            title: $title
            description: $description
            teamId: $teamId
            labelIds: [$labelId]
            subscriberIds: $subscriberIds
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
        subscriberIds=subscriber_ids,
    )
