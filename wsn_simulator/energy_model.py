from config import Config

def transmit_energy(distance, packet_size=Config.PACKET_SIZE):
    if distance <= Config.D0:
        return packet_size * Config.E_ELEC + packet_size * Config.E_FS * (distance ** 2)
    return packet_size * Config.E_ELEC + packet_size * Config.E_MP * (distance ** 4)

def receive_energy(packet_size=Config.PACKET_SIZE):
    return packet_size * Config.E_ELEC

def aggregate_energy(num_signals, packet_size=Config.PACKET_SIZE):
    return Config.E_DA * packet_size * num_signals

def sensing_energy(packet_size=Config.PACKET_SIZE):
    return packet_size * Config.E_ELEC