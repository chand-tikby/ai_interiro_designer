import uuid
from typing import List
from app.schemas.design import RoomDesignRequest, RoomDesignResponse, DesignRecommendation


class InteriorDesignService:
    @staticmethod
    def generate_recommendations(request: RoomDesignRequest) -> RoomDesignResponse:
        design_id = str(uuid.uuid4())
        
        # Default starter recommendations based on requested style
        sample_recommendations: List[DesignRecommendation] = [
            DesignRecommendation(
                category="Furniture",
                item_name=f"{request.style.capitalize()} accent sofa and coffee table",
                suggested_color="Neutral beige / light oak",
                notes="Keep low profile for a clean silhouette.",
            ),
            DesignRecommendation(
                category="Lighting",
                item_name="Dimmable floor standing lamp with warm LED",
                suggested_color="Matte black / Brass",
                notes="Layer ambient light at 2700K color temperature.",
            ),
            DesignRecommendation(
                category="Decor",
                item_name="Potted indoor plants (Fiddle Leaf Fig or Monstera)",
                suggested_color="Natural green / Terracotta pot",
                notes="Adds vitality and organic texture to the space.",
            ),
        ]
        
        return RoomDesignResponse(
            status="success",
            message=f"Generated {request.style} design plan for {request.room_type}.",
            design_id=design_id,
            style=request.style,
            room_type=request.room_type,
            recommendations=sample_recommendations,
            generated_image_url=None,  # Ready to hook into diffusion/image model pipeline
        )


interior_service = InteriorDesignService()

