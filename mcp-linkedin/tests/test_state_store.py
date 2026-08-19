"""
Testes do armazenamento de state (anti-CSRF) do OAuth LinkedIn.

Nenhum destes testes acessa rede, LinkedIn, ou usa qualquer
credencial. O tempo e controlado por um relogio falso injetado no
StateStore, para o comportamento de expiracao ser deterministico.
"""

from mcp_linkedin.auth_linkedin.state_store import StateStore


class FakeClock:
    """Relogio controlavel manualmente, para testes deterministicos."""

    def __init__(self, start: float = 0.0):
        self._now = start

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds


def test_state_gerado_tem_entropia_adequada():
    store = StateStore(clock=FakeClock())
    valores = {store.generate() for _ in range(50)}

    assert len(valores) == 50
    assert all(len(v) >= 32 for v in valores)


def test_state_recem_criado_e_valido():
    store = StateStore(clock=FakeClock())
    state = store.generate()

    assert store.validate_and_consume(state) is True


def test_state_inexistente_e_rejeitado():
    store = StateStore(clock=FakeClock())

    assert store.validate_and_consume("state-que-nunca-existiu") is False


def test_state_expirado_e_rejeitado():
    clock = FakeClock()
    store = StateStore(ttl_seconds=600, clock=clock)
    state = store.generate()

    clock.advance(601)

    assert store.validate_and_consume(state) is False


def test_state_valido_so_pode_ser_consumido_uma_vez():
    store = StateStore(clock=FakeClock())
    state = store.generate()

    assert store.validate_and_consume(state) is True
    assert store.validate_and_consume(state) is False


def test_segundo_uso_do_mesmo_state_e_rejeitado_mesmo_apos_falha():
    clock = FakeClock()
    store = StateStore(ttl_seconds=600, clock=clock)
    state = store.generate()
    clock.advance(601)

    primeira_tentativa = store.validate_and_consume(state)
    segunda_tentativa = store.validate_and_consume(state)

    assert primeira_tentativa is False
    assert segunda_tentativa is False


def test_multiplos_states_podem_coexistir():
    store = StateStore(clock=FakeClock())
    a = store.generate()
    b = store.generate()
    c = store.generate()

    assert store.validate_and_consume(b) is True
    assert store.validate_and_consume(a) is True
    assert store.validate_and_consume(c) is True


def test_um_state_nao_valida_outro():
    store = StateStore(clock=FakeClock())
    store.generate()
    valor_nunca_emitido = "valor-arbitrario-nao-emitido"

    assert store.validate_and_consume(valor_nunca_emitido) is False


def test_armazenamento_nao_persiste_em_disco():
    store_a = StateStore(clock=FakeClock())
    state = store_a.generate()

    store_b = StateStore(clock=FakeClock())

    assert store_b.validate_and_consume(state) is False


def test_nenhuma_chamada_externa_e_realizada(monkeypatch):
    import socket

    def bloquear_rede(*args, **kwargs):
        raise AssertionError("state_store nao deve abrir conexao de rede")

    monkeypatch.setattr(socket.socket, "connect", bloquear_rede)

    store = StateStore(clock=FakeClock())
    state = store.generate()
    store.validate_and_consume(state)
