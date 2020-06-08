UPDATE data_quality.sources SET source = 'calculation_attribute_preprocess' WHERE source = 'processing_attributes';
UPDATE data_quality.sources SET source = 'calculation_attribute_postprocess' WHERE source = 'processing_campaigns';
INSERT into data_quality.sources (`source`) VALUES ('calculation_attribute');