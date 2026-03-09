from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from database import engine, Base
from schema import schema

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Doctor Appointment Network",
    description="GraphQL API for students to book campus medical appointments",
    version="1.0.0"
)

# Add GraphQL router with GraphiQL interface
graphql_app = GraphQLRouter(schema, graphiql=True)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Doctor Appointment Network API",
        "graphql_endpoint": "/graphql",
        "graphiql_interface": "/graphql",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
