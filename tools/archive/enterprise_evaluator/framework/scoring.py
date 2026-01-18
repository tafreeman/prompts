from .dimensions import Dimension, PerformanceLevel, EvaluationResult

def calculate_weighted_score(results: list[EvaluationResult], dimensions: list[Dimension]) -> float:
    """
    Calculate the final weighted score based on dimension results.
    """
    total_score = 0.0
    total_weight = 0.0
    
    # Map dimensions by ID for easy lookup
    dim_map = {d.id: d for d in dimensions}
    
    for res in results:
        if res.dimension_id in dim_map:
            weight = dim_map[res.dimension_id].weight
            total_score += res.score * weight
            total_weight += weight
            
    if total_weight == 0:
        return 0.0
        
    return round(total_score / total_weight, 2)

def determine_performance_level(score: float) -> PerformanceLevel:
    if score >= 90:
        return PerformanceLevel.EXCEPTIONAL
    elif score >= 80:
        return PerformanceLevel.PROFICIENT
    elif score >= 70:
        return PerformanceLevel.COMPETENT
    elif score >= 60:
        return PerformanceLevel.DEVELOPING
    else:
        return PerformanceLevel.INADEQUATE
