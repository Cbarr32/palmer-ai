"""Evidence-based validation and confidence scoring framework"""
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from datetime import datetime
import statistics

from ...utils.logger import get_logger

logger = get_logger(__name__)

class EvidenceLevel(int, Enum):
    DIRECT_OBSERVATION = 1  # Screenshot, direct API data
    CREDIBLE_RESEARCH = 2   # Verified third-party sources
    PATTERN_RECOGNITION = 3 # Inferred from multiple data points
    INFORMED_SPECULATION = 4 # Expert assessment with uncertainty
    
class EvidenceQuality(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    
class Evidence:
    def __init__(self,
                 evidence_type: str,
                 content: Any,
                 source: str,
                 level: EvidenceLevel,
                 confidence: float = 0.0,
                 timestamp: Optional[datetime] = None):
        self.evidence_type = evidence_type
        self.content = content
        self.source = source
        self.level = level
        self.confidence = confidence
        self.timestamp = timestamp or datetime.utcnow()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.evidence_type,
            "content": self.content,
            "source": self.source,
            "level": self.level.value,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat()
        }
        
class EvidenceValidator:
    """Validates and scores evidence for analysis conclusions"""
    
    def __init__(self):
        self.evidence_weights = {
            EvidenceLevel.DIRECT_OBSERVATION: 1.0,
            EvidenceLevel.CREDIBLE_RESEARCH: 0.85,
            EvidenceLevel.PATTERN_RECOGNITION: 0.70,
            EvidenceLevel.INFORMED_SPECULATION: 0.50
        }
        
    def validate_evidence(self, evidence: Evidence) -> Tuple[bool, List[str]]:
        """Validate individual evidence item"""
        errors = []
        
        # Check required fields
        if not evidence.source:
            errors.append("Evidence source is required")
        if not evidence.content:
            errors.append("Evidence content is required")
        if evidence.confidence < 0 or evidence.confidence > 1:
            errors.append("Confidence must be between 0 and 1")
            
        # Validate based on evidence level
        if evidence.level == EvidenceLevel.DIRECT_OBSERVATION:
            if not self._validate_direct_observation(evidence):
                errors.append("Direct observation lacks verifiable data")
        elif evidence.level == EvidenceLevel.CREDIBLE_RESEARCH:
            if not self._validate_credible_source(evidence):
                errors.append("Source credibility could not be verified")
                
        return len(errors) == 0, errors
        
    def calculate_evidence_strength(self, evidence_list: List[Evidence]) -> float:
        """Calculate overall strength of evidence collection"""
        if not evidence_list:
            return 0.0
            
        weighted_scores = []
        
        for evidence in evidence_list:
            weight = self.evidence_weights[evidence.level]
            score = evidence.confidence * weight
            weighted_scores.append(score)
            
        return statistics.mean(weighted_scores)
        
    def triangulate_evidence(self, 
                           evidence_list: List[Evidence],
                           min_sources: int = 2) -> Dict[str, Any]:
        """Triangulate evidence from multiple sources"""
        triangulation = {
            "verified_claims": [],
            "conflicting_claims": [],
            "single_source_claims": [],
            "confidence_score": 0.0
        }
        
        # Group evidence by claim/type
        claims = {}
        for evidence in evidence_list:
            claim_key = f"{evidence.evidence_type}:{evidence.content}"
            if claim_key not in claims:
                claims[claim_key] = []
            claims[claim_key].append(evidence)
            
        # Analyze each claim
        for claim_key, evidences in claims.items():
            if len(evidences) >= min_sources:
                # Check for consistency
                sources = {e.source for e in evidences}
                if self._check_consistency(evidences):
                    triangulation["verified_claims"].append({
                        "claim": claim_key,
                        "sources": list(sources),
                        "confidence": self.calculate_evidence_strength(evidences)
                    })
                else:
                    triangulation["conflicting_claims"].append({
                        "claim": claim_key,
                        "sources": list(sources),
                        "conflicts": self._identify_conflicts(evidences)
                    })
            else:
                triangulation["single_source_claims"].append({
                    "claim": claim_key,
                    "source": evidences[0].source,
                    "confidence": evidences[0].confidence
                })
                
        # Calculate overall confidence
        if triangulation["verified_claims"]:
            triangulation["confidence_score"] = statistics.mean([
                claim["confidence"] for claim in triangulation["verified_claims"]
            ])
            
        return triangulation
        
    def generate_evidence_trail(self, 
                              analysis_chain: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate audit trail of evidence for analysis conclusions"""
        trail = []
        
        for step in analysis_chain:
            trail_entry = {
                "step": step.get("step_name", "Unknown"),
                "timestamp": step.get("timestamp", datetime.utcnow().isoformat()),
                "evidence_used": [],
                "confidence": 0.0,
                "reasoning": step.get("reasoning", "")
            }
            
            # Extract evidence from step
            if "evidence" in step:
                for evidence_data in step["evidence"]:
                    evidence = Evidence(**evidence_data)
                    valid, errors = self.validate_evidence(evidence)
                    
                    trail_entry["evidence_used"].append({
                        "evidence": evidence.to_dict(),
                        "valid": valid,
                        "validation_errors": errors
                    })
                    
            # Calculate step confidence
            if trail_entry["evidence_used"]:
                valid_evidence = [
                    Evidence(**e["evidence"]) 
                    for e in trail_entry["evidence_used"] 
                    if e["valid"]
                ]
                trail_entry["confidence"] = self.calculate_evidence_strength(valid_evidence)
                
            trail.append(trail_entry)
            
        return trail
        
    def _validate_direct_observation(self, evidence: Evidence) -> bool:
        """Validate direct observation evidence"""
        # Check for screenshot, API response, or other direct data
        return bool(evidence.content) and evidence.source.startswith(("http", "api:", "screenshot:"))
        
    def _validate_credible_source(self, evidence: Evidence) -> bool:
        """Validate credible research source"""
        credible_domains = [
            ".gov", ".edu", ".org",
            "reuters.com", "bloomberg.com", "wsj.com",
            "nature.com", "science.org", "ieee.org"
        ]
        
        source_lower = evidence.source.lower()
        return any(domain in source_lower for domain in credible_domains)
        
    def _check_consistency(self, evidences: List[Evidence]) -> bool:
        """Check if multiple evidence items are consistent"""
        # Simple consistency check - can be made more sophisticated
        contents = [str(e.content) for e in evidences]
        return len(set(contents)) == 1
        
    def _identify_conflicts(self, evidences: List[Evidence]) -> List[Dict[str, Any]]:
        """Identify conflicts in evidence"""
        conflicts = []
        
        # Compare each pair of evidence
        for i in range(len(evidences)):
            for j in range(i + 1, len(evidences)):
                if str(evidences[i].content) != str(evidences[j].content):
                    conflicts.append({
                        "source1": evidences[i].source,
                        "content1": str(evidences[i].content),
                        "source2": evidences[j].source,
                        "content2": str(evidences[j].content)
                    })
                    
        return conflicts
        
class ConfidenceCalibrator:
    """Calibrates confidence scores based on evidence and historical accuracy"""
    
    def __init__(self):
        self.calibration_history: List[Dict[str, Any]] = []
        
    def calibrate_confidence(self,
                           raw_confidence: float,
                           evidence_strength: float,
                           complexity_factor: float = 1.0) -> float:
        """Calibrate confidence score based on multiple factors"""
        # Base calibration
        calibrated = raw_confidence * evidence_strength
        
        # Adjust for complexity
        calibrated = calibrated / complexity_factor
        
        # Apply historical calibration if available
        if self.calibration_history:
            historical_adjustment = self._calculate_historical_adjustment()
            calibrated = calibrated * historical_adjustment
            
        # Ensure within bounds
        return max(0.0, min(1.0, calibrated))
        
    def record_outcome(self,
                      prediction: Dict[str, Any],
                      actual_outcome: Dict[str, Any]):
        """Record prediction outcome for calibration improvement"""
        self.calibration_history.append({
            "prediction": prediction,
            "outcome": actual_outcome,
            "timestamp": datetime.utcnow(),
            "accuracy": self._calculate_accuracy(prediction, actual_outcome)
        })
        
    def _calculate_historical_adjustment(self) -> float:
        """Calculate adjustment factor based on historical accuracy"""
        if not self.calibration_history:
            return 1.0
            
        recent_history = self.calibration_history[-50:]  # Last 50 predictions
        accuracies = [entry["accuracy"] for entry in recent_history]
        
        avg_accuracy = statistics.mean(accuracies)
        
        # If consistently overconfident, reduce confidence
        if avg_accuracy < 0.7:
            return 0.85
        # If consistently underconfident, increase confidence
        elif avg_accuracy > 0.9:
            return 1.1
        else:
            return 1.0
            
    def _calculate_accuracy(self, 
                          prediction: Dict[str, Any],
                          outcome: Dict[str, Any]) -> float:
        """Calculate accuracy of a prediction"""
        # Simple accuracy calculation - can be made domain-specific
        correct_predictions = 0
        total_predictions = 0
        
        for key, predicted_value in prediction.items():
            if key in outcome:
                total_predictions += 1
                if predicted_value == outcome[key]:
                    correct_predictions += 1
                    
        return correct_predictions / total_predictions if total_predictions > 0 else 0.0
