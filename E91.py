from qiskit import QuantumCircuit, Aer, execute
from scipy.optimize import minimize_scalar
from qiskit.visualization import plot_histogram, circuit_drawer

import numpy as np

def generate_secret_key(length):
    # Generate a random binary string as the secret key
    return ''.join([str(np.random.randint(2)) for _ in range(length)])

def create_entangled_pairs(num_pairs):
    # Create EPR pairs (Bell pairs) using Hadamard and CNOT gates
    qc = QuantumCircuit(2, 2)
    for _ in range(num_pairs):
        qc.h(0)
        qc.cx(0, 1)
        qc.barrier()
    return qc

def measure_epr_pairs(qc, num_pairs):
    # Measure EPR pairs in the Bell basis
    bell_measurement_circuits = []
    for i in range(num_pairs):
        bell_measurement_circuit = QuantumCircuit(2, 2)
        bell_measurement_circuit.cx(0, 1)
        bell_measurement_circuit.h(0)
        bell_measurement_circuit.measure([0, 1], [0, 1])
        bell_measurement_circuits.append(bell_measurement_circuit)
    return bell_measurement_circuits

def calculate_qber(counts, total_shots):
    # Calculate Quantum Bit Error Rate (QBER)
    total_errors = counts.get('01', 0) + counts.get('10', 0)
    qber = total_errors / total_shots
    return qber
def calculate_secret_key_rate(num_pairs, qber):
    # Calculate Secret Key Rate using the E91 protocol
    error_corrected_length = num_pairs * (1 - qber)
    secret_key_rate = error_corrected_length / num_pairs
    return secret_key_rate

def calculate_adversarial_resilience(num_pairs, qber):
    # Calculate Adversarial Resilience using the E91 protocol
    def objective_function(alpha):
        return np.exp(-2 * alpha) - (1 - qber) ** num_pairs

    optimal_alpha = minimize_scalar(objective_function).x
    adversarial_resilience = 1 - np.exp(-2 * optimal_alpha)
    return adversarial_resilience

def main():
    # Parameters
    num_pairs = 10
    total_shots = 1024

    # Step 1: Alice prepares entangled pairs (EPR pairs)
    alice_entangled_pairs = create_entangled_pairs(num_pairs)

    # Step 2: Bob measures entangled pairs in the Bell basis
    bell_measurement_circuits = measure_epr_pairs(alice_entangled_pairs, num_pairs)
    
    circuit_drawer(alice_entangled_pairs, style='mpl', output='mpl', filename='e91_circuit.png')


    # Step 3: Simulate the measurement of EPR pairs
    simulator = Aer.get_backend('qasm_simulator')
    qber_values = []
    for bell_measurement_circuit in bell_measurement_circuits:
        job = execute(bell_measurement_circuit, simulator, shots=total_shots)
        result = job.result()
        counts = result.get_counts(bell_measurement_circuit)
        qber = calculate_qber(counts, total_shots)
        qber_values.append(qber)

    # Step 4: Calculate average QBER
    avg_qber = np.mean(qber_values)

    # Step 5: Calculate Secret Key Rate
    secret_key_rate = calculate_secret_key_rate(num_pairs, avg_qber)

    # Step 6: Calculate Adversarial Resilience
    adversarial_resilience = calculate_adversarial_resilience(num_pairs, avg_qber)

    # Print results
    print("Average Quantum Bit Error Rate (QBER):", avg_qber)
    print("Secret Key Rate:", secret_key_rate)
    print("Adversarial Resilience:", adversarial_resilience)

if __name__ == "__main__":
    main()