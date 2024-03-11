from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram, circuit_drawer
import numpy as np

def bb84_circuit(secret_key):
    # Create a Quantum Circuit for BB84 Protocol
    qc = QuantumCircuit(2, 2)

    # Encoding Alice's Secret Key Bits
    for i, bit in enumerate(secret_key):
        if bit == '1':
            qc.x(i)  # Apply X gate if the bit is 1
    qc.barrier()

    # Prepare random bases for measurement
    qc.h(0)  # Apply Hadamard gate for basis X
    qc.measure([0, 1], [0, 1])  # Measure qubits and store results in classical bits

    return qc

def calculate_qber(counts, total_shots):
    # Calculate Quantum Bit Error Rate (QBER)
    total_errors = counts.get('10', 0) + counts.get('01', 0)  # Errors occur when basis do not match
    qber = total_errors / total_shots
    return qber

def calculate_key_generation_rate(total_shots, execution_time, key_length):
    # Calculate Key Generation Rate
    key_generation_rate = key_length / execution_time
    return key_generation_rate

# Generate a random secret key
secret_key = ''.join([str(np.random.randint(2)) for _ in range(2)])

# Create the circuit
bb84_circuit = bb84_circuit(secret_key)

# Simulate the circuit
simulator = Aer.get_backend('qasm_simulator')
job = execute(bb84_circuit, simulator, shots=1000)
result = job.result()
counts = result.get_counts(bb84_circuit)

# Calculate QBER
total_shots = sum(counts.values())
qber = calculate_qber(counts, total_shots)

# Calculate Key Generation Rate (Assuming 1 execution takes 1 second)
execution_time = 1
key_length = len(secret_key)
key_generation_rate = calculate_key_generation_rate(total_shots, execution_time, key_length)

# Print results
print("Quantum Bit Error Rate (QBER):", qber)
print("Key Generation Rate:", key_generation_rate, "key bits per second")

# Draw the circuit
circuit_drawer(bb84_circuit, style='mpl', output='mpl', filename='bb84.png')

