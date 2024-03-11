
from qiskit import QuantumCircuit, Aer, execute, IBMQ
from qiskit.visualization import plot_histogram, circuit_drawer
import numpy as np

IBMQ.save_account('e306ef2b96396af97bb83db62cc782278717c308b4cf0a8610303c32811d887a5c0f7ceead3aa39881040dcc00a194c4e0516d6c980cf65b56e3a54d6dd54d91')

def generate_secret_key(length):
    # Generate a random binary string as the secret key
    return ''.join([str(np.random.randint(2)) for _ in range(length)])

def quantum_teleportation_circuit(secret_key):
    # Create a quantum circuit with 3 qubits and 3 classical bits
    qc = QuantumCircuit(3, 3)

    # Step 1: Prepare a Bell pair
    qc.h(1)             # Apply a Hadamard gate to qubit 1
    qc.cx(1, 2)         # Apply a CNOT gate with qubit 1 as control and qubit 2 as target
    qc.barrier()        # Barrier to separate steps visually

    # Step 2: Prepare the quantum state to be teleported
    for i, bit in enumerate(secret_key):
        if bit == '1':
            qc.x(0)         # Apply X gate to qubit 0 if the bit in Alice's secret key is 1
        qc.h(0)             # Apply a Hadamard gate to qubit 0
        qc.cx(0, 1)         # Apply a CNOT gate with qubit 0 as control and qubit 1 as target
        qc.barrier()        # Barrier to separate steps visually

    # Step 3: Perform a Bell measurement
    qc.cx(0, 1)         # Apply a CNOT gate with qubit 0 as control and qubit 1 as target
    qc.h(0)             # Apply a Hadamard gate to qubit 0
    qc.measure([0, 1], [0, 1])  # Measure qubits 0 and 1, store the result in classical bits 0 and 1
    qc.barrier()        # Barrier to separate steps visually

    # Step 4: Perform corrections based on measurement results
    for i, bit in enumerate(secret_key):
        if bit == '1':
            qc.z(2)         # Apply Z gate to qubit 2 if the bit in Alice's secret key is 1
        qc.x(2).c_if(1, 1) # Apply X gate to qubit 2 if classical bit 1 is 1
        qc.z(2).c_if(0, 1) # Apply Z gate to qubit 2 if classical bit 0 is 1
        qc.measure(2, 2)   # Measure qubit 2 and store the result in classical bit 2

    return qc

def simulate_teleportation(qc):
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend=simulator, shots=1024).result()
    counts = result.get_counts(qc)
    return counts

def main():
    # Generate a random secret key
    secret_key = generate_secret_key(3)  # Length of the secret key

    # Create the quantum teleportation circuit
    teleported_qc = quantum_teleportation_circuit(secret_key)
    print(teleported_qc)

    # Simulate the quantum teleportation process
    counts = simulate_teleportation(teleported_qc)

    # Display the measurement results using a histogram
    print("Measurement results:", counts)
    plot_histogram(counts)
    
    # Plot the circuihttps://file+.vscode-resource.vscode-cdn.net/Users/ayonsomaddar/Chandigarh%20University/Projects/Quantum_Info/Quantum-Leap/teleportation_circuit.png?version%3D1709964773380t
    circuit_drawer(teleported_qc, style='mpl', output='mpl', filename='teleportation_circuit.png')

if __name__ == "__main__":
    main()
