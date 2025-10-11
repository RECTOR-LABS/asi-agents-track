'use client';

import { AlertTriangle, CheckCircle, Info, AlertCircle, Activity } from 'lucide-react';
import clsx from 'clsx';

interface DiagnosticData {
  condition: string;
  confidence: number;
  urgency: 'emergency' | 'urgent' | 'routine';
  symptoms: string[];
  treatment_plan?: {
    recommended_actions?: string[];
    medications?: string[];
    follow_up?: string;
  };
  reasoning_chain?: string[];
  differential_diagnoses?: string[];
  red_flags?: string[];
}

interface DiagnosticReportProps {
  data: DiagnosticData;
  className?: string;
}

const urgencyConfig = {
  emergency: {
    label: 'EMERGENCY - Seek immediate medical attention',
    icon: AlertTriangle,
    color: 'emergency',
    bgColor: 'bg-emergency-50',
    borderColor: 'border-emergency-500',
    textColor: 'text-emergency-700',
    iconColor: 'text-emergency-600',
  },
  urgent: {
    label: 'URGENT - Schedule appointment within 24-48 hours',
    icon: AlertCircle,
    color: 'urgent',
    bgColor: 'bg-urgent-50',
    borderColor: 'border-urgent-500',
    textColor: 'text-urgent-700',
    iconColor: 'text-urgent-600',
  },
  routine: {
    label: 'ROUTINE - Schedule regular appointment',
    icon: CheckCircle,
    color: 'routine',
    bgColor: 'bg-routine-50',
    borderColor: 'border-routine-500',
    textColor: 'text-routine-700',
    iconColor: 'text-routine-600',
  },
};

export default function DiagnosticReport({ data, className }: DiagnosticReportProps) {
  const config = urgencyConfig[data.urgency] || urgencyConfig.routine;
  const Icon = config.icon;

  return (
    <div className={clsx('bg-white rounded-lg shadow-lg overflow-hidden animate-slideUp', className)}>
      {/* Urgency Banner */}
      <div
        className={clsx(
          'px-6 py-4 border-l-4 flex items-center gap-3',
          config.bgColor,
          config.borderColor
        )}
      >
        <Icon className={clsx('w-6 h-6', config.iconColor)} />
        <div>
          <p className={clsx('font-semibold text-sm', config.textColor)}>{config.label}</p>
          <p className="text-xs text-gray-600 mt-0.5">
            Confidence: {(data.confidence * 100).toFixed(0)}%
          </p>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Primary Diagnosis */}
        <section>
          <h3 className="text-lg font-semibold text-gray-900 mb-2 flex items-center gap-2">
            <Activity className="w-5 h-5 text-primary-600" />
            Primary Diagnosis
          </h3>
          <p className="text-2xl font-bold text-primary-600">{data.condition}</p>
        </section>

        {/* Red Flags (if any) */}
        {data.red_flags && data.red_flags.length > 0 && (
          <section className="bg-emergency-50 border border-emergency-200 rounded-lg p-4">
            <h3 className="text-base font-semibold text-emergency-800 mb-2 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" />
              Critical Warning Signs
            </h3>
            <ul className="space-y-1">
              {data.red_flags.map((flag, idx) => (
                <li key={idx} className="text-sm text-emergency-700 flex items-start gap-2">
                  <span className="text-emergency-600 mt-0.5">•</span>
                  <span>{flag}</span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* Symptoms Analyzed */}
        {data.symptoms && data.symptoms.length > 0 && (
          <section>
            <h3 className="text-base font-semibold text-gray-900 mb-2">Symptoms Analyzed</h3>
            <div className="flex flex-wrap gap-2">
              {data.symptoms.map((symptom, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-primary-50 text-primary-700 rounded-full text-sm font-medium"
                >
                  {symptom}
                </span>
              ))}
            </div>
          </section>
        )}

        {/* Treatment Plan */}
        {data.treatment_plan && (
          <section>
            <h3 className="text-base font-semibold text-gray-900 mb-3">Treatment Recommendations</h3>

            {/* Recommended Actions */}
            {data.treatment_plan.recommended_actions && data.treatment_plan.recommended_actions.length > 0 && (
              <div className="mb-4">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Recommended Actions:</h4>
                <ul className="space-y-2">
                  {data.treatment_plan.recommended_actions.map((action, idx) => (
                    <li key={idx} className="text-sm text-gray-600 flex items-start gap-2">
                      <CheckCircle className="w-4 h-4 text-routine-600 flex-shrink-0 mt-0.5" />
                      <span>{action}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Medications */}
            {data.treatment_plan.medications && data.treatment_plan.medications.length > 0 && (
              <div className="mb-4">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Medications:</h4>
                <ul className="space-y-2">
                  {data.treatment_plan.medications.map((med, idx) => (
                    <li key={idx} className="text-sm text-gray-600 flex items-start gap-2">
                      <span className="text-primary-600 mt-0.5">•</span>
                      <span>{med}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Follow Up */}
            {data.treatment_plan.follow_up && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <h4 className="text-sm font-medium text-blue-900 mb-1 flex items-center gap-2">
                  <Info className="w-4 h-4" />
                  Follow-Up Care:
                </h4>
                <p className="text-sm text-blue-800">{data.treatment_plan.follow_up}</p>
              </div>
            )}
          </section>
        )}

        {/* Differential Diagnoses */}
        {data.differential_diagnoses && data.differential_diagnoses.length > 0 && (
          <section>
            <h3 className="text-base font-semibold text-gray-900 mb-2">Alternative Diagnoses</h3>
            <p className="text-sm text-gray-600 mb-3">
              Other conditions with similar symptoms that were considered:
            </p>
            <div className="space-y-2">
              {data.differential_diagnoses.map((diagnosis, idx) => (
                <div
                  key={idx}
                  className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700"
                >
                  {diagnosis}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Reasoning Chain */}
        {data.reasoning_chain && data.reasoning_chain.length > 0 && (
          <section>
            <h3 className="text-base font-semibold text-gray-900 mb-2">Diagnostic Reasoning</h3>
            <p className="text-sm text-gray-600 mb-3">
              How the AI system arrived at this diagnosis:
            </p>
            <ol className="space-y-2">
              {data.reasoning_chain.map((step, idx) => (
                <li key={idx} className="text-sm text-gray-700 flex items-start gap-3">
                  <span className="flex-shrink-0 w-6 h-6 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center text-xs font-semibold">
                    {idx + 1}
                  </span>
                  <span className="flex-1 pt-0.5">{step}</span>
                </li>
              ))}
            </ol>
          </section>
        )}

        {/* Disclaimer */}
        <section className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <p className="text-xs text-gray-600 leading-relaxed">
            <strong className="text-gray-900">Medical Disclaimer:</strong> This diagnostic report is generated by an AI system for informational and educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
          </p>
        </section>
      </div>
    </div>
  );
}
